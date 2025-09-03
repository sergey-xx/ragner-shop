import logging
from asgiref.sync import async_to_sync, sync_to_async

from django.db.models import Sum

from payments.activators import aactivate_code_kokos, aactivate_code_fars, aactivate_code
from bot.tasks import send_notification_task
from backend.config import URL_CONFIG
from backend.celery import app

from .models import UcCode, Activator
from orders.models import Order

logger = logging.getLogger(__name__)


async def check_order(order: Order):
    codes = await UcCode.objects.filter(order=order, is_success=True).aaggregate(Sum('amount'))
    order_amount = order.data.get('amount')
    ready_amount = codes.get('amount__sum', 0) or 0
    logger.info(f'{order.id=} {order_amount=} {ready_amount=}')
    if order_amount >= ready_amount:
        order.is_completed = True
        await order.asave(update_fields=('is_completed',))


async def activate_code(code: UcCode, pubg_id: str):
    logger.info(f'Activating code {code.code} for user {pubg_id}')
    if code.activator == Activator.KOKOS:
        succ, status = await aactivate_code_kokos(pubg_id, code.code)
    elif code.activator == Activator.UCODEIUM:
        succ, status = await aactivate_code(pubg_id, code.code, uc_value=code.amount)
    elif code.activator == Activator.FARS:
        succ, status = await aactivate_code_fars(pubg_id, code.code, uc_value=code.amount, order_id=code.order.id)
        logger.info(f'Ответ FARS {status}. Успех: {succ}.')
        if succ:
            logger.info('Откладываем дальнейшее действие до поступления webhook')
            return
    else:
        logger.warning(f'Для кода {code.id=} не задан активатор')
        return
    await process_result(code, succ, status)


async def process_result(code: UcCode, succ: bool, status: str):
    code.is_activated = True
    code.status = status
    await code.asave(update_fields=('is_activated', 'status'))
    text = (f'{"✅" if succ else "❗️"} '
            f'Activating code {code.code} {"" if succ else "NOT"} '
            f'activated with status {status}')
    logger.info(text)
    chat_id = await sync_to_async(lambda: URL_CONFIG.ADMIN_ID)()
    send_notification_task.delay(chat_id, text)
    code.is_success = succ
    await code.asave(update_fields=('is_success',))
    if not succ:
        code.order.is_completed = False
        await code.order.asave(update_fields=('is_completed',))
    await check_order(code.order)


@app.task()
def activate_code_task(code: str):
    uccode = UcCode.objects.select_related('order__item', 'order__tg_user').get(code=code)
    if not uccode.is_activated and uccode.order and uccode.order.pubg_id:
        logger.info(f'Got activation task! code: {code}')
        async_to_sync(activate_code)(uccode, uccode.order.pubg_id)

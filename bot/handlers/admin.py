import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from django.conf import settings

from bot.callbacks import OrderCD
from orders.models import Order
from users.models import TgUser

ENV = settings.ENV
PUBG_ID_LEN = 5

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.callback_query(OrderCD.filter(F.action == OrderCD.Action.complete))
async def make_order_completed(query: CallbackQuery, callback_data: OrderCD, state: FSMContext):
    is_admin = await TgUser.objects.filter(tg_id=query.from_user.id, is_admin=True).aexists()
    if not is_admin:
        text = f'Not admin can not complete the task {callback_data.id}'
        await query.answer(text)
        logger.info(text)
        return
    order = await Order.objects.aget(id=callback_data.id)
    order.is_completed = True
    await order.asave(update_fields=('is_completed',))
    text = f'{query.message.text}\n✅'
    await query.message.edit_text(text=text, reply_markup=None)


@router.callback_query(OrderCD.filter(F.action == OrderCD.Action.cancel))
async def make_order_cancelled(query: CallbackQuery, callback_data: OrderCD, state: FSMContext):
    is_admin = await TgUser.objects.filter(tg_id=query.from_user.id, is_admin=True).aexists()
    if not is_admin:
        text = f'Not admin can not cancel the task {callback_data.id}'
        await query.answer(text)
        logger.info(text)
        return
    order = await Order.objects.aget(id=callback_data.id)
    await order.acancel()
    text = f'{await order.aadmin_str()}'
    await query.message.edit_text(
        text=text,
    )


@router.message(F.text == '/regchat')
async def get_group_chat_id(message: Message, state: FSMContext):
    logger.info(f'ID чата для регистрации {message.chat.id}')
    is_admin = await TgUser.objects.filter(tg_id=message.from_user.id, is_admin=True).aexists()
    if is_admin:
        await message.answer(f'Your CHAT ID {message.chat.id}')

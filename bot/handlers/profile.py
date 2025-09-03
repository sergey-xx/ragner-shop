from datetime import timedelta
from decimal import Decimal

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async
from django.conf import settings
from django.utils import timezone
from django.core.paginator import Paginator

import bot.keyboards as kb
from backend.config import PAYMENT_CONFIG
from bot.callbacks import HistoryCD, MenuCD, ProfileCD
from bot.states import TopUpState
from users.models import TgUser
from orders.models import TopUp, Order

ENV = settings.ENV

router = Router(name=__name__)


@router.callback_query(MenuCD.filter(F.category == MenuCD.Category.profile))
async def get_profile(query: CallbackQuery, callback_data: MenuCD, state: FSMContext):
    await query.message.edit_text(text='Choose category', reply_markup=await kb.get_profile_inline())


@router.callback_query(ProfileCD.filter(F.category == ProfileCD.Category.HISOTORY))
async def get_history(query: CallbackQuery, callback_data: MenuCD, state: FSMContext):
    # tg_user = await TgUser.objects.aget(tg_id=query.from_user.id)
    # orders = await sync_to_async(lambda: list(Order.objects.filter(tg_user=tg_user)))()
    # order_text = '\n'.join([order.to_str() for order in orders])
    # await query.message.edit_text(
    #     text=f'There your orders history:\n{order_text}', reply_markup=await kb.get_history_inline()
    # )
    await query.message.edit_text('Choose category', reply_markup=await kb.get_history_inline())


@router.callback_query(HistoryCD.filter(F.category))
async def get_history_slice(query: CallbackQuery, callback_data: HistoryCD, state: FSMContext):
    tg_user = await TgUser.objects.aget(tg_id=query.from_user.id)
    target_date = timezone.now() - timedelta(days=callback_data.category)
    orders = await sync_to_async(lambda: list(Order.objects.filter(tg_user=tg_user, created_at__gte=target_date)))()
    paginator = Paginator(orders, 25)
    p = paginator.page(callback_data.page)
    order_text = '\n'.join([order.to_str() for order in p.object_list])
    text = (f'There your orders history for last {callback_data.category} days:\n\n' f'{order_text}')
    await query.message.edit_text(
        text,
        reply_markup=await kb.get_paginated_inline(
            p.has_previous(),
            p.has_next(),
            callback_data,
            back_to=ProfileCD(category=ProfileCD.Category.HISOTORY)
        )
    )


@router.callback_query(ProfileCD.filter((F.category == ProfileCD.Category.POINTS) & (F.action == None)))  # NOQA
async def get_points(query: CallbackQuery, callback_data: MenuCD, state: FSMContext):
    tg_user = await TgUser.objects.aget(tg_id=query.from_user.id)
    show_redeem = tg_user.points > tg_user.POINTS_RATIO
    await query.message.edit_text(
        text=f'You have {tg_user.points} points', reply_markup=await kb.get_points_inline(show_redeem)
    )


@router.callback_query(ProfileCD.filter((F.category == ProfileCD.Category.BALANCE) & (F.action == None)))  # NOQA
async def get_balance(query: CallbackQuery, callback_data: MenuCD, state: FSMContext):
    tg_user = await TgUser.objects.aget(tg_id=query.from_user.id)
    await query.message.edit_text(text=f'You have {tg_user.balance} USD', reply_markup=await kb.get_balance_inline())


@router.callback_query(ProfileCD.filter(F.action == 'topup'))
async def ask_topup_amount(query: CallbackQuery, callback_data: MenuCD, state: FSMContext):
    await state.set_state(TopUpState.amount)
    await query.message.edit_text('Write topup amount')


@router.message(TopUpState.amount)
async def gen_topup(message: Message, state: FSMContext):
    try:
        text = message.text.replace(',', '.')
        amount = float(text)
        if amount < 1:
            await message.answer("Min amount 1 USDT.")
            return
    except Exception:
        await message.answer("Can't understand amount. Please try again.")
        return
    topup, _ = await TopUp.objects.aget_or_create(
        tg_user=await TgUser.objects.aget(tg_id=message.from_user.id),
        amount=Decimal(str(amount)).quantize(Decimal('0.001')),
        is_paid=False,
        is_topped=False
    )
    text = (f'Please topup exactly that amount: {topup.to_pay}\n'
            f'{await sync_to_async(lambda: PAYMENT_CONFIG.PAYMENT_TEXT)()}\n'
            f'<b>Valid for {await sync_to_async(lambda: PAYMENT_CONFIG.TOPUP_LIFETIME)()} hours</b>')
    await message.answer(text, parse_mode='HTML')
    await state.clear()


@router.callback_query(ProfileCD.filter((F.category == ProfileCD.Category.POINTS) & (F.action)))
async def redeem_points(query: CallbackQuery, callback_data: MenuCD, state: FSMContext):
    tg_user = await TgUser.objects.aget(tg_id=query.from_user.id)
    res = await tg_user.aredeem_points()
    if res:
        await tg_user.arefresh_from_db()
        await query.message.edit_text(
            text=f'You have {tg_user.points} points', reply_markup=await kb.get_points_inline(False)
        )
        return
    await query.answer(f'You do not have enough points to redeem. Min amount: {tg_user.POINTS_RATIO}', show_alert=True)

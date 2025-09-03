from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async
from django.conf import settings

import bot.keyboards as kb
from backend.config import TEXT_CONFIG
from bot.callbacks import MenuCD
from users.models import TgUser

ENV = settings.ENV
PUBG_ID_LEN = 5

router = Router(name=__name__)


@router.message(CommandStart(), F.chat.type == 'private')
async def start(message: Message, state: FSMContext):
    await state.clear()
    tg_user = await TgUser.objects.filter(tg_id=message.from_user.id).afirst()
    if not tg_user:
        await TgUser.objects.acreate(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        text = await sync_to_async(lambda: TEXT_CONFIG.HI_MSG)()
        await message.answer(text)
    text = await sync_to_async(lambda: TEXT_CONFIG.MENU_MSG)()
    await message.answer(text, reply_markup=await kb.get_menu_inline())


@router.callback_query(MenuCD.filter(F.category == 'root'))
async def get_menu(query: CallbackQuery, callback_data: MenuCD, state: FSMContext):
    text = await sync_to_async(lambda: TEXT_CONFIG.MENU_MSG)()
    await query.message.edit_text(text, reply_markup=await kb.get_menu_inline())

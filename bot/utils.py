import io
import logging

from aiogram import Bot
from aiogram.types import BufferedInputFile
from asgiref.sync import sync_to_async, async_to_sync

from backend.settings import ENV
from codes.models import StockbleCode
from users.models import TgUser

logger = logging.getLogger(__name__)


@sync_to_async
def get_all_admins_id() -> list:
    return list(TgUser.objects
                .filter(tg_id__isnull=False)
                .filter(is_admin=True)
                .values_list('tg_id', flat=True))


def generate_codes_text(codes: list[StockbleCode]):
    text = '\n'.join([f'{code.code}' for code in codes])
    return f'Your codes:\n{text}'


def generate_file(text: str, filename: str):
    file_buffer = io.BytesIO(text.encode('utf-8'))
    file_buffer.seek(0)
    return BufferedInputFile(file_buffer.read(), filename=filename)


async def send_codes_to_user(bot: Bot, chat_id: int, codes: list[StockbleCode]):
    async with Bot(ENV.str('TG_TOKEN_BOT')) as bot:
        text = generate_codes_text(codes)
        if text:
            if len(text) > 3500:
                document = generate_file(text, 'codes.txt')
                await bot.send_document(chat_id=chat_id, document=document, caption='There your codes')
                return
            await bot.send_message(chat_id, text=f'There your codes:\n{text}')


async def asend_notification(chat_id: int, text: str, reply_markup=None, message_id=None):
    async with Bot(ENV.str('TG_TOKEN_BOT')) as bot:
        if message_id:
            try:
                await bot.edit_message_text(
                    text=text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup
                )
            except Exception as e:
                logger.error(f'{e}')
                logger.error(f'Message {message_id} in chat {chat_id} cant be edited. Sending new')
                await bot.send_message(chat_id, text=text, reply_markup=reply_markup)
        else:
            try:
                await bot.send_message(chat_id, text=text, reply_markup=reply_markup)
            except Exception as e:
                logger.error(f'Message has not been delivered to {chat_id}')
                logger.error(f'{e}')


@async_to_sync
async def send_notification(chat_id: int, text: str, reply_markup=None, message_id=None):
    return await asend_notification(chat_id, text, reply_markup, message_id)


async def asend_text_or_txt(bot, chat_id, text):
    if len(text) > 3500:
        document = generate_file(text, 'codes.txt')
        await bot.send_document(
            chat_id=chat_id, document=document, caption='Codes are in file'
        )
        return
    await bot.send_message(chat_id, text=text)

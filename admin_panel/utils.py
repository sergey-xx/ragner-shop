import logging
from io import BytesIO

from aiogram import Bot
from aiogram.types import BufferedInputFile

from backend.settings import ENV
from bot.utils import get_all_admins_id

logger = logging.getLogger('Import')


async def get_file_id(file, file_type: str):

    if not file:
        return None

    if isinstance(file.file, BytesIO):
        file_input = BufferedInputFile(file.file.getvalue(), filename=file.name)
    else:
        bytes_file = BytesIO(file.read())
        file_input = BufferedInputFile(bytes_file.getvalue(), filename=file.name)

    file_id = -1
    admins = await get_all_admins_id()
    async with Bot(token=ENV('TG_TOKEN_BOT')) as bot:
        if len(admins) != 0:
            if file_type == 'image':
                message = await bot.send_photo(chat_id=admins[0], photo=file_input)
                file_id = message.photo[-1].file_id
                await message.delete()
            elif file_type == "video":
                message = await bot.send_video(chat_id=admins[0], video=file_input)
                file_id = message.video.file_id
                await message.delete()
            else:
                message = await bot.send_document(chat_id=admins[0], document=file_input)
                file_id = message.document.file_id
                await message.delete()
        return file_id

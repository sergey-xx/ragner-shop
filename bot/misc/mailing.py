import logging
import asyncio

from aiogram import Bot, exceptions
from aiogram.types import InputMediaDocument, InputMediaPhoto, InputMediaVideo
from asgiref.sync import sync_to_async
from django.utils import timezone

from admin_panel.models import Attachment, Mailing
from users.models import TgUser

logger = logging.getLogger(__name__)


async def start_mailing(bot: Bot):
    now = timezone.now()
    input_media = {
        Attachment.FileType.DOCUMENT: InputMediaDocument,
        Attachment.FileType.PHOTO: InputMediaPhoto,
        Attachment.FileType.VIDEO: InputMediaVideo
    }
    users = await sync_to_async(lambda: list(TgUser.objects.all()))()
    mailings = await sync_to_async(lambda: list(Mailing.objects.filter(date_time__lte=now, is_sent=False)))()
    for mailing in mailings:
        await mailing.arefresh_from_db()
        if mailing.is_sent:
            continue
        mailing.is_sent = True
        await mailing.asave(update_fields=('is_sent',))
        logger.info(f'Mailing {mailing.id} started')
        attachments = await sync_to_async(lambda: list(Attachment.objects.filter(mailing=mailing)))()
        users_ = list(users)
        while users_:
            try:
                user = users_[-1]
                if len(attachments) == 0:
                    await bot.send_message(chat_id=user.tg_id, text=mailing.text)
                elif len(attachments) > 0:
                    att_list = [
                        input_media[attachment.file_type](media=attachment.file_id) for attachment in attachments
                    ]
                    att_list[-1].caption = mailing.text
                    await bot.send_media_group(chat_id=user.tg_id, media=att_list)
                users_.pop()
            except exceptions.TelegramRetryAfter as e:
                logger.warning(f'Flood limit is exceeded. Sleep {e.retry_after} seconds.')
                await asyncio.sleep(e.retry_after)
            except (exceptions.TelegramForbiddenError, exceptions.TelegramBadRequest) as e:
                users_.pop()
                logger.error(f'Seems like user {user.username} {user.tg_id} has blocked the bot')
                logger.error(f'{e}')

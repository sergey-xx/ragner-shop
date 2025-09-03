import logging

from aiogram import Bot
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from admin_panel.models import Attachment, Mailing
from users.models import TgUser
from aiogram.types import BufferedInputFile
from io import BytesIO

logger = logging.getLogger(__name__)


async def send_file(chat_id, file, file_type: str):
    file_id = -1
    async with Bot(settings.ENV.str('TG_TOKEN_BOT')) as bot:
        if isinstance(file.file, BytesIO):
            file_input = BufferedInputFile(file.file.getvalue(), filename=file.name)
        else:
            bytes_file = BytesIO(file.read())
            file_input = BufferedInputFile(bytes_file.getvalue(), filename=file.name)
        if file_type == Attachment.FileType.PHOTO:
            message = await bot.send_photo(chat_id, photo=file_input)
            file_id = message.photo[-1].file_id
            await message.delete()
        elif file_type == Attachment.FileType.VIDEO:
            message = await bot.send_video(chat_id, video=file_input)
            file_id = message.video.file_id
            await message.delete()
        elif file_type == Attachment.FileType.DOCUMENT:
            message = await bot.send_document(chat_id, document=file_input)
            file_id = message.document.file_id
            await message.delete()
    return file_id


@receiver(post_save, sender=Attachment)
def preload_file(sender, instance: Attachment, created, **kwargs):
    admin = TgUser.objects.filter(is_admin=True).first()
    if not admin:
        logger.error('You need at least one admin to send attachment')
        return
    if not instance.file_id:
        instance.file_id = async_to_sync(send_file)(admin.tg_id, file=instance.file, file_type=instance.file_type)
        instance.save()


@receiver(post_save, sender=Mailing)
def validate_att(sender, instance: Mailing, created, **kwargs):
    if instance.date_time:
        all_types = set([attachment.file_type for attachment in instance.attachments.all()])
        if Attachment.FileType.DOCUMENT in all_types and len(all_types) > 1:
            instance.date_time = None
            instance.save()

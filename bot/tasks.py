import logging
from bot.utils import send_notification

from bot.keyboards import KEYBOARDS

from backend.celery import app

logger = logging.getLogger(__name__)


@app.task()
def send_notification_task(chat_id, text, keyboard: str | None = None, kwargs=None, message_id=None):
    """Фоново отправляем сообщение."""
    if not chat_id:
        logger.error('Message cant be sent! chat_id is None')
    logger.info('Have task to send message')
    kwargs = kwargs or {}
    reply_markup = KEYBOARDS.get_func(keyboard)(**kwargs) if keyboard else None
    send_notification(chat_id, text, reply_markup=reply_markup, message_id=message_id)

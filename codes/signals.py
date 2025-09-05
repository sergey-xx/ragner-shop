import logging

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UcCode
from .tasks import activate_code_task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=UcCode)
def uccode_post_save(sender, instance: UcCode, created, **kwargs):
    if not instance.is_activated and instance.order and instance.order.pubg_id:
        logger.info(f"Have code to activate: {instance.code}. Sending to Celery.")
        transaction.on_commit(
            lambda: activate_code_task.delay(instance.code)
        )
        logger.info(
            f'Code {instance.code} was attached to order #{instance.order.id}. '
            f'Activation task has been scheduled to run on transaction commit.'
        )

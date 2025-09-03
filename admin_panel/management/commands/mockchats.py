from django.core.management import BaseCommand

from admin_panel.models import ManagerChat

from backend.config import URL_CONFIG


def mock_chats():
    if not ManagerChat.objects.filter(tg_id=URL_CONFIG.ADMIN_ID).exists():
        ManagerChat.objects.create(
            title='Test managers chat',
            tg_id=URL_CONFIG.ADMIN_ID
        )


class Command(BaseCommand):

    def handle(self, *args, **options):
        mock_chats()

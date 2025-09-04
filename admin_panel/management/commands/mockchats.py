from django.core.management import BaseCommand

from admin_panel.models import ManagerChat
from backend.config import URL_CONFIG


def mock_chats():
    if not ManagerChat.objects.filter(tg_id=URL_CONFIG.ADMIN_ID).exists():
        ManagerChat.objects.create(
            title="Test managers chat", tg_id=URL_CONFIG.ADMIN_ID
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Checking/creating manager chat...")
        mock_chats()
        self.stdout.write(self.style.SUCCESS("Manager chat is set up."))

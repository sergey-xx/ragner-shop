import random
import string

from django.core.management import BaseCommand

from backend.constants import DEFAULT_SC_AMOUNTS
from codes.models import StockbleCode


def random_string(n: int) -> str:
    """Генерирует случайную строку длиной n символов."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=n))


def mock_stock_codes():
    for amount in DEFAULT_SC_AMOUNTS.keys():
        for i in range(10):
            code = random_string(10)
            StockbleCode.objects.create(code=code, amount=amount)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Generating mock stockable codes...")
        mock_stock_codes()
        self.stdout.write(self.style.SUCCESS("Successfully created mock codes."))

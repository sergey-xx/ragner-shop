from decimal import Decimal

from asgiref.sync import sync_to_async
from django.db import models, transaction


class TgUser(models.Model):
    """Класс Пользователей ТГ."""

    tg_id = models.PositiveBigIntegerField(
        unique=True,
        verbose_name="Telegram ID",
        db_index=True,
    )
    username = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Telegram username"
    )
    first_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="First name"
    )
    last_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Last Name"
    )
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updation date")
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Balance"
    )
    points = models.IntegerField(default=0, verbose_name="Points")
    POINTS_RATIO = 1000

    @property
    def is_authenticated(self):
        return True

    class Meta:
        verbose_name = "Telegram user"
        verbose_name_plural = "Telegram users"
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.first_name} {self.last_name}/{self.id}"

    def redeem_points(self):
        if self.points < self.POINTS_RATIO:
            return False
        with transaction.atomic():
            tg_user = TgUser.objects.select_for_update().get(id=self.id)
            balance_redeem = tg_user.points // tg_user.POINTS_RATIO
            points_to_return = tg_user.points % tg_user.POINTS_RATIO
            tg_user.balance += balance_redeem
            tg_user.points = points_to_return
            tg_user.save()
            return True

    async def aredeem_points(self):
        return await sync_to_async(self.redeem_points)()

    def process_payment(self, amount: Decimal | int | float):
        with transaction.atomic():
            tg_user = TgUser.objects.select_for_update().get(id=self.id)
            tg_user.balance += amount
            if tg_user.balance < 0:
                raise ValueError("Balance cant be less than zero")
            tg_user.save()
            if amount < 0:
                new_points = -amount
                tg_user.points += new_points
                tg_user.save(update_fields=("points",))

    async def aprocess_payment(self, amount: Decimal | int | float):
        return await sync_to_async(self.process_payment)(amount)

    def get_or_generate_api_key(self):
        from api.models import APIKey

        api_key, created = APIKey.objects.get_or_create(user=self)
        return api_key.key

    async def aget_or_generate_api_key(self):
        return await sync_to_async(self.get_or_generate_api_key)()

    def regenerate_api_key(self):
        from api.models import APIKey

        APIKey.objects.filter(user=self).delete()
        new_key = APIKey.objects.create(user=self)
        return new_key.key

    async def aregenerate_api_key(self):
        return await sync_to_async(self.regenerate_api_key)()

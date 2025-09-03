from django.db import models

from backend.constants import DEFAULT_SC_AMOUNTS, DEFAULT_UC_AMOUNTS


class Activator(models.TextChoices):
    KOKOS = 'kokos', 'Kokos'
    FARS = 'fars', 'FARS'
    SMILEONE = 'smileone', 'SmileOne'
    UCODEIUM = 'ucodeium', 'UCodeium'


class AbstractCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Code')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updation date')

    class Meta:
        abstract = True


class UcCode(AbstractCode):

    amount = models.PositiveIntegerField(choices=DEFAULT_UC_AMOUNTS, verbose_name='Nominal')
    status = models.CharField(max_length=50, blank=True, null=True, verbose_name='API status')
    is_activated = models.BooleanField(default=False, verbose_name='Is used')
    is_success = models.BooleanField(blank=True, null=True, verbose_name='Is activated successfully')
    activator = models.CharField(
        blank=True, null=True, choices=Activator, verbose_name='Activator', help_text='if not selected, then any'
    )
    order = models.ForeignKey('orders.Order',
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE,
                              related_name='uc_codes',
                              verbose_name='Order')

    class Meta:
        verbose_name = 'UC activating code'
        verbose_name_plural = 'UC activating codes'


class StockbleCode(AbstractCode):

    amount = models.IntegerField(choices=DEFAULT_SC_AMOUNTS, verbose_name='Nominal')
    order = models.ForeignKey('orders.Order',
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE,
                              related_name='stockble_codes',
                              verbose_name='Order')

    class Meta:
        verbose_name = 'PUBG STOCKBLE CODE'
        verbose_name_plural = 'PUBG STOCKBLE CODES'


class Giftcard(AbstractCode):
    order = models.ForeignKey('orders.Order',
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE,
                              related_name='giftcard_codes',
                              verbose_name='Order')
    item = models.ForeignKey(
        'items.GiftcardItem',
        on_delete=models.PROTECT,
        related_name='giftcard_codes',
        verbose_name='Item in menu')

    class Meta:
        verbose_name = 'GIFTCARD'
        verbose_name_plural = 'GIFTCARDS'

from django.db import models

from asgiref.sync import sync_to_async

from codes.models import StockbleCode, UcCode, Activator
from admin_panel.models import ManagerChat
from backend.constants import DEFAULT_UC_AMOUNTS, CODES_MAP


class Item(models.Model):

    class Category(models.TextChoices):
        PUBG_UC = 'pubg_uc', 'PUBG UC'
        CODES = 'codes', 'GIFTCARDS & CODES'
        POPULARITY = 'popularity', 'Popularity'
        HOME_VOTE = 'home_vote', 'HOME VOTE'
        OFFERS = 'offers', 'Offers'
        GIFTCARD = 'giftcard', 'Giftcard'
        STARS = 'stars', 'Telegram Stars'
        DIAMOND = 'diamond', 'Mobilelegends diamond'

    title = models.CharField(
        blank=True, null=True, verbose_name='Title',
        help_text='Not obligatory. Has priority in the display in the menu'
    )
    category = models.CharField(blank=True, max_length=50, choices=Category, verbose_name='Category')
    price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='Price')
    amount = models.IntegerField(
        blank=True, null=True, choices=DEFAULT_UC_AMOUNTS, verbose_name='Amount', help_text='For codes and popularity'
    )
    is_active = models.BooleanField(default=False, verbose_name='Active?')
    activator = models.CharField(
        blank=True, null=True, choices=Activator,
        verbose_name='Activator', help_text='if not selected, then manual activation'
    )
    data = models.JSONField(blank=True, null=True, verbose_name='Additional data')
    chat = models.ForeignKey(
        ManagerChat, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='items', verbose_name='Chat for notifications',
    )
    folder = models.ForeignKey(
        'Folder', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='items', verbose_name='Folder'
    )

    class Meta:
        ordering = ["price", "title",]

    def __str__(self) -> str:
        return f'{self.value} | {self.price}$'

    @classmethod
    def items(cls, **kwargs):
        return cls.objects.filter(is_active=True, **kwargs)

    @classmethod
    async def aitems(cls, **kwargs):
        return await sync_to_async(lambda: list(cls.items(**kwargs)))()

    @classmethod
    def have_active_items(cls):
        return cls.items().exists()

    @classmethod
    async def ahave_active_items(cls):
        return await sync_to_async(cls.have_active_items)()

    @property
    def value(self):
        if self.category == Item.Category.PUBG_UC:
            return (self.title or f'{self.amount} UC')
        if self.category == Item.Category.CODES:
            return (self.title or f'{self.amount} UC')
        if self.category == Item.Category.POPULARITY:
            return (self.title or f'{self.amount} Popularity')
        return f'{self.title}'

    def to_dict(self):
        return {
            'title': self.title,
            'value': self.value,
            'category': self.category,
            'price': str(self.price),
            'amount': self.amount,
            'is_active': self.is_active,
            'activator': self.activator,
        }

    def get_total_price(self, quantity: int):
        return self.price * quantity

    def get_stock_amount(self):
        if self.category == Item.Category.CODES:
            return StockbleCode.objects.filter(amount=self.amount, order__isnull=True).count()
        if self.category == Item.Category.GIFTCARD:
            return self.giftcard_codes.filter(order__isnull=True).count()
        if self.category == Item.Category.PUBG_UC:
            nominals = CODES_MAP[self.amount]
            counter = [
                int(
                    UcCode.objects.filter(
                        models.Q(activator=self.activator) | models.Q(activator__isnull=True),
                        order__isnull=True,
                        amount=nom,
                    ).count() / nominals.count(nom)
                )
                for nom in nominals
            ]
            return min(counter)
        return None

    async def aget_stock_amount(self):
        return await sync_to_async(self.get_stock_amount)()


class PUBGUCItem(Item):

    class Meta:
        proxy = True
        verbose_name = "PUBG UC"
        verbose_name_plural = "PUBG UC Items"

    def __str__(self) -> str:
        return f'{self.value} | {self.price}$'

    @classmethod
    def items(cls, **kwargs):
        return super().items(category=cls.Category.PUBG_UC, **kwargs)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.category = Item.Category.PUBG_UC
        return super().save(force_insert, force_update, using, update_fields)


class StockCodesItem(Item):

    class Meta:
        proxy = True
        verbose_name = 'STOCKBLE CODES'
        verbose_name_plural = 'STOCKBLE CODES'

    @classmethod
    def items(cls, **kwargs):
        return super().items(category=cls.Category.CODES, **kwargs).order_by('amount')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.category = Item.Category.CODES
        return super().save(force_insert, force_update, using, update_fields)


class GiftcardItem(Item):

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.category = Item.Category.GIFTCARD
        return super().save(force_insert, force_update, using, update_fields)

    @classmethod
    def items(cls, **kwargs):
        return super().items(category=cls.Category.GIFTCARD, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "Giftcards item"
        verbose_name_plural = "Giftcards items"


class PopularityItem(Item):

    class Meta:
        proxy = True
        verbose_name = "Popularity"
        verbose_name_plural = "Popularity Items"

    @classmethod
    def items(cls, **kwargs):
        return super().items(category=cls.Category.POPULARITY, **kwargs)
        # return cls.objects.filter(category=cls.Category.POPULARITY, is_active=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.category = Item.Category.POPULARITY
        return super().save(force_insert, force_update, using, update_fields)


class HomeVoteItem(Item):

    class Meta:
        proxy = True
        verbose_name = "HOME VOTE"
        verbose_name_plural = "HOME VOTE Items"

    @classmethod
    def items(cls, **kwargs):
        return super().items(category=cls.Category.HOME_VOTE, **kwargs)
        # return cls.objects.filter(category=cls.Category.HOME_VOTE, is_active=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.category = Item.Category.HOME_VOTE
        return super().save(force_insert, force_update, using, update_fields)


class OffersItem(Item):

    class Meta:
        proxy = True
        verbose_name = "Offer"
        verbose_name_plural = "Offers Items"

    @classmethod
    def items(cls, **kwargs):
        return super().items(category=cls.Category.OFFERS, **kwargs)
        # return cls.objects.filter(category=cls.Category.OFFERS, is_active=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.category = Item.Category.OFFERS
        return super().save(force_insert, force_update, using, update_fields)


class StarItem(Item):

    class Meta:
        proxy = True
        verbose_name = "Star"
        verbose_name_plural = "Star Items"

    @classmethod
    def items(cls, **kwargs):
        return super().items(category=cls.Category.STARS, **kwargs)
        # return cls.objects.filter(category=cls.Category.STARS, is_active=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.category = Item.Category.STARS
        return super().save(force_insert, force_update, using, update_fields)


class DiamondItem(Item):

    class Meta:
        proxy = True
        verbose_name = "MLBB Russia"
        verbose_name_plural = "MLBB Russia"

    @classmethod
    def items(cls, **kwargs):
        return super().items(category=cls.Category.DIAMOND, **kwargs)
        # return cls.objects.filter(category=cls.Category.DIAMOND, is_active=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.category = Item.Category.DIAMOND
        return super().save(force_insert, force_update, using, update_fields)


class Folder(models.Model):

    category = models.CharField(
        blank=True,
        max_length=50,
        default=Item.Category.CODES,
        choices=Item.Category,
        verbose_name='Category'
    )
    title = models.CharField(
        max_length=35,
        verbose_name='Title'
    )
    ordering_id = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Ordering num'
    )

    def aitems(self, **kwargs):
        return sync_to_async(lambda: list(self.items.filter(**kwargs)))()

    @classmethod
    def get(cls, **kwargs):
        return cls.objects.filter(**kwargs)

    @classmethod
    async def aget(cls, **kwargs):
        return await sync_to_async(lambda: list(cls.get(**kwargs)))()

    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"
        ordering = ["ordering_id", "category", "id",]

    def __str__(self) -> str:
        return f'{Item.Category(self.category).label} | {self.title}'

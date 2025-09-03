from django.contrib import admin

from .models import (DiamondItem, Folder, GiftcardItem, HomeVoteItem, Item,
                     OffersItem, PopularityItem, PUBGUCItem, StarItem,
                     StockCodesItem)


@admin.register(PUBGUCItem)
class PUBGUCItemAdmin(admin.ModelAdmin):
    list_display = (
        'value',
        'title',
        'price',
        'amount',
        'is_active',
        'activator',
    )
    readonly_fields = ('category', 'data',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.PUBG_UC)


@admin.register(StockCodesItem)
class StockCodesItemAdmin(admin.ModelAdmin):
    list_display = (
        'value',
        'title',
        'price',
        'amount',
        'is_active',
        'folder',
    )
    readonly_fields = ('category', )
    exclude = ('activator', 'data',)
    list_editable = (
        'folder',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.CODES)


@admin.register(GiftcardItem)
class GiftcardItemAdmin(admin.ModelAdmin):
    list_display = (
        'value',
        'title',
        'price',
        'folder',
        'is_active',
    )
    readonly_fields = ('category',)
    exclude = ('amount', 'activator', 'data',)
    list_editable = ('folder',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.GIFTCARD)


@admin.register(PopularityItem)
class PopularityItemAdmin(admin.ModelAdmin):
    list_display = (
        'value',
        'title',
        'price',
        'amount',
        'is_active',
    )
    readonly_fields = ('category',)
    exclude = ('activator', 'data',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.POPULARITY)


@admin.register(HomeVoteItem)
class HomeVoteItemAdmin(admin.ModelAdmin):
    list_display = (
        'value',
        'title',
        'price',
        'amount',
        'is_active',
    )
    readonly_fields = ('category',)
    exclude = ('amount', 'activator', 'data',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.HOME_VOTE)


@admin.register(OffersItem)
class OffersItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'is_active',
    )
    readonly_fields = ('category',)
    exclude = ('amount', 'activator', 'data',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.OFFERS)


@admin.register(StarItem)
class StarItemAdmin(admin.ModelAdmin):
    list_display = (
        'value',
        'title',
        'price',
        'amount',
        'is_active',
    )
    readonly_fields = ('category',)
    exclude = ('amount', 'activator', 'data',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.STARS)


@admin.register(DiamondItem)
class DiamondAdmin(admin.ModelAdmin):
    list_display = (
        'value',
        'title',
        'price',
        'is_active',
    )
    readonly_fields = ('category', 'data',)
    exclude = ('amount', 'activator',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.DIAMOND)


@admin.register(Folder)
class Folderdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'ordering_id',
        'category',
    )
    list_editable = (
        'ordering_id',
    )
    readonly_fields = ('category',)

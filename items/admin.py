from django.contrib import admin

from .models import (
    DiamondItem,
    Folder,
    GiftcardItem,
    HomeVoteItem,
    Item,
    ManualCategory,
    ManualItem,
    MorePubgItem,
    OffersItem,
    PopularityItem,
    PUBGUCItem,
    StarItem,
    StockCodesItem,
)


@admin.register(PUBGUCItem)
class PUBGUCItemAdmin(admin.ModelAdmin):
    list_display = (
        "value",
        "title",
        "price",
        "amount",
        "is_active",
        "activator",
    )
    readonly_fields = (
        "category",
        "data",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.PUBG_UC)


@admin.register(StockCodesItem)
class StockCodesItemAdmin(admin.ModelAdmin):
    list_display = (
        "value",
        "title",
        "price",
        "amount",
        "is_active",
        "folder",
    )
    readonly_fields = ("category",)
    exclude = (
        "activator",
        "data",
    )
    list_editable = ("folder",)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.CODES)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "folder":
            kwargs["queryset"] = Folder.objects.filter(category=Item.Category.CODES)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(GiftcardItem)
class GiftcardItemAdmin(admin.ModelAdmin):
    list_display = (
        "value",
        "title",
        "price",
        "folder",
        "is_active",
    )
    readonly_fields = ("category",)
    exclude = (
        "amount",
        "activator",
        "data",
    )
    list_editable = ("folder",)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.GIFTCARD)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "folder":
            kwargs["queryset"] = Folder.objects.filter(category=Item.Category.CODES)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PopularityItem)
class PopularityItemAdmin(admin.ModelAdmin):
    list_display = (
        "value",
        "title",
        "price",
        "is_active",
    )
    readonly_fields = ("category",)
    exclude = ("amount", "activator", "data", "manual_category", "folder")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(category=Item.Category.POPULARITY, folder__isnull=True)
        )


@admin.register(HomeVoteItem)
class HomeVoteItemAdmin(admin.ModelAdmin):
    list_display = (
        "value",
        "title",
        "price",
        "is_active",
    )
    readonly_fields = ("category",)
    exclude = ("amount", "activator", "data", "manual_category", "folder")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(category=Item.Category.HOME_VOTE, folder__isnull=True)
        )


@admin.register(OffersItem)
class OffersItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "is_active",
    )
    readonly_fields = ("category",)
    exclude = ("amount", "activator", "data", "manual_category", "folder")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(category=Item.Category.OFFERS, manual_category__isnull=True)
        )


@admin.register(StarItem)
class StarItemAdmin(admin.ModelAdmin):
    list_display = (
        "value",
        "title",
        "price",
        "amount",
        "is_active",
    )
    readonly_fields = ("category",)
    exclude = (
        "amount",
        "activator",
        "data",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.STARS)


@admin.register(DiamondItem)
class DiamondAdmin(admin.ModelAdmin):
    list_display = (
        "value",
        "title",
        "price",
        "is_active",
    )
    readonly_fields = (
        "category",
        "data",
    )
    exclude = (
        "amount",
        "activator",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=Item.Category.DIAMOND)


@admin.register(MorePubgItem)
class MorePubgItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "folder",
        "is_active",
    )
    list_filter = ("folder", "is_active")
    list_editable = ("folder",)
    exclude = ("amount", "activator", "data", "manual_category")
    readonly_fields = ("category",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(folder__category=Item.Category.MORE_PUBG)
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "folder":
            kwargs["queryset"] = Folder.objects.filter(category=Item.Category.MORE_PUBG)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["folder"].required = True
        return form


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "ordering_id",
        "category",
    )
    list_editable = ("ordering_id", "category")
    list_filter = ("category",)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "category":
            allowed_categories = [
                Item.Category.CODES.value,
                Item.Category.MORE_PUBG.value,
            ]
            kwargs["choices"] = [
                (value, label)
                for value, label in db_field.choices
                if value in allowed_categories
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)


@admin.register(ManualCategory)
class ManualCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "prompt_text", "is_active", "ordering")
    list_editable = ("is_active", "ordering")


@admin.register(ManualItem)
class ManualItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "manual_category", "is_active")
    list_filter = ("manual_category", "is_active")
    readonly_fields = ("category",)
    exclude = ("amount", "activator", "data", "folder")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(manual_category__isnull=False)

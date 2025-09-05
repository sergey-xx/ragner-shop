from django.contrib import admin
from django.urls import reverse

from .forms import GiftCardImportForm, ImportForm, StockbleCodeImportForm
from .models import ActivatorPriority, Giftcard, StockbleCode, UcCode


@admin.register(ActivatorPriority)
class ActivatorPriorityAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(UcCode)
class UcCodeAdmin(admin.ModelAdmin):
    change_list_template = "admin/custom_change_list.html"
    list_filter = (
        "amount",
        "is_priority_use",
        "activator",
        "status",
    )
    list_display = (
        "code",
        "amount",
        "is_priority_use",
        "order",
        "activator",
        "status",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "status",
        "is_activated",
        "order",
    )

    def changelist_view(self, request, extra_content=None):
        extra_content = extra_content or {}
        extra_content["form"] = ImportForm
        extra_content["revese_url"] = reverse("import_codes")
        return super().changelist_view(request, extra_content)


@admin.register(StockbleCode)
class StockbleCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "amount",
        "order",
    )
    change_list_template = "admin/custom_change_list.html"

    def changelist_view(self, request, extra_content=None):
        extra_content = extra_content or {}
        extra_content["form"] = StockbleCodeImportForm
        extra_content["revese_url"] = reverse("import_stockblecode")
        return super().changelist_view(request, extra_content)


@admin.register(Giftcard)
class GiftcardAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "code",
        "order",
    )
    change_list_template = "admin/custom_change_list.html"
    readonly_fields = ("order",)

    def changelist_view(self, request, extra_content=None):
        extra_content = extra_content or {}
        extra_content["form"] = GiftCardImportForm
        extra_content["revese_url"] = reverse("import_giftcards")
        return super().changelist_view(request, extra_content)

from django.contrib import admin

from .forms import ImportForm, GiftCardImportForm, StockbleCodeImportForm
from .models import StockbleCode, UcCode, Giftcard

from django.urls import reverse


@admin.register(UcCode)
class UcCodeAdmin(admin.ModelAdmin):

    change_list_template = "admin/custom_change_list.html"
    list_filter = (
        'amount',
    )
    list_display = (
        'code',
        'amount',
        'order',
        'activator',
        'status',
        'created_at',
        'updated_at',
    )
    readonly_fields = (
        'status',
        'is_activated',
        'order',
    )

    def changelist_view(self, request, extra_content=None):
        extra_content = extra_content or {}
        extra_content['form'] = ImportForm
        extra_content['revese_url'] = reverse('import_codes')
        return super().changelist_view(request, extra_content)


@admin.register(StockbleCode)
class StockbleCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'amount',
        'order',
    )
    change_list_template = "admin/custom_change_list.html"

    def changelist_view(self, request, extra_content=None):
        extra_content = extra_content or {}
        extra_content['form'] = StockbleCodeImportForm
        extra_content['revese_url'] = reverse('import_stockblecode')
        return super().changelist_view(request, extra_content)


@admin.register(Giftcard)
class GiftcardAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'code',
        'order',
    )
    change_list_template = "admin/custom_change_list.html"
    readonly_fields = ('order',)

    def changelist_view(self, request, extra_content=None):
        extra_content = extra_content or {}
        extra_content['form'] = GiftCardImportForm
        extra_content['revese_url'] = reverse('import_giftcards')
        return super().changelist_view(request, extra_content)

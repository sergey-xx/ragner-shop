from django.contrib import admin

from .models import Order, TopUp


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'tg_user',
        'is_completed',
        'item',
        'quantity',
        'created_at',
        'updated_at',
        'data',
        'price',
        'pubg_id',
    )

    list_filter = (
        'is_completed',
        'tg_user',
    )

    readonly_fields = (
        'tg_user',
        'item',
        'quantity',
        'created_at',
        'updated_at',
        'data',
        'price',
        'category',
        'pubg_id',
    )


@admin.register(TopUp)
class TopUpAdmin(admin.ModelAdmin):

    list_display = (
        'tg_user',
        'amount',
        'comission',
        'to_pay',
        'tx_id',
        'is_paid',
        'is_topped',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'tg_user',
    )
    readonly_fields = (
        'tg_user',
        'amount',
        'comission',
        'to_pay',
        'tx_id',
        'is_topped',
        'created_at',
        'updated_at',
        'paid_at',
    )

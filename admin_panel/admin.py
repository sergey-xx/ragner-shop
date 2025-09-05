from datetime import datetime

from django.contrib import admin
from django.db.models import Count, Sum
from django.forms import ModelForm
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.utils.timezone import now

from codes.models import Giftcard, StockbleCode, UcCode
from items.models import Item
from orders.models import Order

from .models import Attachment, DailyReport, Mailing, ManagerChat


@admin.register(ManagerChat)
class ManagerChatAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "tg_id",
    )


class AttachmentInlineAdmin(admin.TabularInline):
    """Class to inline Attachment."""

    model = Attachment
    fields = (
        "file_type",
        "file",
        "file_id",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    inlines = (AttachmentInlineAdmin,)

    def save_form(self, request: HttpRequest, form: ModelForm, change: bool):
        return super().save_form(request, form, change)


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/daily_report.html"

    def changelist_view(self, request, extra_context=None):
        context = self.admin_site.each_context(request)

        report_date_str = request.GET.get("report_date", now().strftime("%Y-%m-%d"))
        try:
            report_date = datetime.strptime(report_date_str, "%Y-%m-%d").date()
        except ValueError:
            report_date = now().date()

        uc_sold_today = (
            UcCode.objects.filter(order__created_at__date=report_date)
            .values("amount")
            .annotate(count=Count("id"))
            .order_by("amount")
        )

        uc_remaining_stock = (
            UcCode.objects.filter(order__isnull=True)
            .values("amount")
            .annotate(count=Count("id"))
            .order_by("amount")
        )

        uc_added_today = (
            UcCode.objects.filter(created_at__date=report_date)
            .values("amount")
            .annotate(count=Count("id"))
            .order_by("amount")
        )

        daily_orders = (
            Order.objects.filter(
                created_at__date=report_date,
                category__in=[Item.Category.GIFTCARD, Item.Category.CODES],
            )
            .select_related("tg_user", "item")
            .order_by("tg_user__username")
        )

        sold_codes_summary = (
            daily_orders.values("item__title", "item__amount")
            .annotate(total_sold=Sum("quantity"))
            .order_by("item__title")
        )

        giftcards_added_today = (
            Giftcard.objects.filter(created_at__date=report_date)
            .values("item__title")
            .annotate(count=Count("id"))
        )

        stockblecodes_added_today = (
            StockbleCode.objects.filter(created_at__date=report_date)
            .values("amount")
            .annotate(count=Count("id"))
        )

        report_data = {
            "report_date": report_date,
            "report_date_str": report_date_str,
            "uc_sold_today": uc_sold_today,
            "uc_remaining_stock": uc_remaining_stock,
            "uc_added_today": uc_added_today,
            "daily_orders_details": daily_orders,
            "sold_codes_summary": sold_codes_summary,
            "giftcards_added_today": giftcards_added_today,
            "stockblecodes_added_today": stockblecodes_added_today,
            "title": "Daily Sales Report",
        }
        context.update(report_data)

        return TemplateResponse(request, self.change_list_template, context)

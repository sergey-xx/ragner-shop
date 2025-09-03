from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest

from .models import Attachment, Mailing, ManagerChat


@admin.register(ManagerChat)
class ManagerChatAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'tg_id',
    )


class AttachmentInlineAdmin(admin.TabularInline):
    """Class to inline Attachment."""

    model = Attachment
    fields = (
        'file_type',
        'file',
        'file_id',
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):

    inlines = (
        AttachmentInlineAdmin,
    )

    def save_form(self, request: HttpRequest, form: ModelForm, change: bool):
        return super().save_form(request, form, change)

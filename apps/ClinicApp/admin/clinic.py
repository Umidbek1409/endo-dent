from django.shortcuts import redirect
from django.urls import reverse
from .base import BaseAdmin
from ..models import ClinicInfo

class ClinicInfoAdmin(BaseAdmin):
    list_display = ("clinic_name", "phone", "email", "action_buttons")
    list_display_links = ("clinic_name",)
    fieldsets = (
        ("Basic Info", {"fields": ("clinic_name", "address", "phone", "working_hours")}),
        ("Social Media", {"fields": ("instagram_url", "telegram_url")}),
        ("Telegram Notifications", {"fields": ("telegram_bot_token", "telegram_chat_id"), "description": "Configure Telegram bot to receive appointment notifications to your personal chat"}),
        ("About Section", {"fields": ("about_text", "about_image")}),
    )

    def has_add_permission(self, request):
        return ClinicInfo.objects.count() < 1

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if ClinicInfo.objects.count() == 1:
            obj = ClinicInfo.objects.first()
            return redirect(reverse("admin:ClinicApp_clinicinfo_change", args=[obj.pk]))
        return super().changelist_view(request, extra_context)

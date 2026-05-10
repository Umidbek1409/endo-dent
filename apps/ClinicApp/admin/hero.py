from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin
from .base import BaseAdmin
from ..models import HeroSection

class HeroSectionAdmin(BaseAdmin):
    list_display = ("headline", "button_text", "is_active", "action_buttons")
    list_display_links = ("headline",)
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("headline", "subheadline", "button_text")
    fieldsets = (
        ("Content", {"fields": ("headline", "subheadline")}),
        ("Call to Action", {"fields": ("button_text", "button_link")}),
        ("Status", {"fields": ("is_active",)}),
    )

    def has_add_permission(self, request):
        return HeroSection.objects.count() < 1

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if HeroSection.objects.count() == 1:
            obj = HeroSection.objects.first()
            return redirect(reverse("admin:ClinicApp_herosection_change", args=[obj.pk]))
        return super().changelist_view(request, extra_context)

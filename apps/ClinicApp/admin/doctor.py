from django.utils.html import format_html
from unfold.decorators import display
from .base import BaseAdmin

class DoctorAdmin(BaseAdmin):
    list_display = ("photo_thumbnail", "full_name", "specialty", "experience_years", "order", "is_visible", "action_buttons")
    list_display_links = ("full_name",)
    list_editable = ("is_visible", "order")
    list_filter = ("is_visible", "specialty")
    search_fields = ("full_name", "specialty", "bio")
    ordering = ("order",)
    fieldsets = (
        ("Personal Info", {"fields": ("full_name", "specialty", "experience_years", "photo")}),
        ("Biography", {"fields": ("bio",)}),
        ("Display", {"fields": ("order", "is_visible")}),
    )

    @display(description="Photo")
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;object-fit:cover;" />',
                obj.photo.url
            )
        return "—"

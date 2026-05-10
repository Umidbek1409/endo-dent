from django.utils.html import format_html
from unfold.decorators import display
from .base import BaseAdmin

class ServiceAdmin(BaseAdmin):
    list_display = ("title", "icon_thumbnail", "order", "is_visible", "action_buttons")
    list_display_links = ("title",)
    list_editable = ("is_visible", "order")
    list_filter = ("is_visible",)
    search_fields = ("title", "description")
    fieldsets = (
        ("Service Details", {"fields": ("title", "description")}),
        ("Media", {"fields": ("icon_image",)}),
        ("Display", {"fields": ("order", "is_visible")}),
    )

    @display(description="Icon")
    def icon_thumbnail(self, obj):
        if obj.icon_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:8px;object-fit:cover;" />',
                obj.icon_image.url
            )
        return "—"

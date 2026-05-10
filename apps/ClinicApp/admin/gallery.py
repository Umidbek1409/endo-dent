from django.utils.html import format_html
from unfold.decorators import display
from .base import BaseAdmin

class GalleryImageAdmin(BaseAdmin):
    list_display = ("image_thumbnail", "caption", "order", "is_visible", "action_buttons")
    list_display_links = ("caption",)
    list_editable = ("order", "is_visible")
    list_filter = ("is_visible",)
    search_fields = ("caption",)
    ordering = ("order",)
    fieldsets = (
        ("Image Details", {"fields": ("image", "caption")}),
        ("Display", {"fields": ("order", "is_visible")}),
    )

    @display(description="Image")
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="50" style="border-radius:8px;object-fit:cover;" />',
                obj.image.url
            )
        return "—"

from django.utils.html import format_html
from unfold.decorators import display
from .base import BaseAdmin

class TestimonialAdmin(BaseAdmin):
    list_display = ("patient_name", "rating_stars", "is_visible", "action_buttons")
    list_display_links = ("patient_name",)
    list_editable = ("is_visible",)
    list_filter = ("is_visible", "rating")
    search_fields = ("patient_name", "review_text")
    fieldsets = (
        ("Patient Info", {"fields": ("patient_name",)}),
        ("Review", {"fields": ("review_text", "rating")}),
        ("Media", {"fields": ("patient_photo",)}),
        ("Status", {"fields": ("is_visible",)}),
    )

    @display(description="Rating")
    def rating_stars(self, obj):
        return format_html(
            '<span class="text-amber-400">{}</span>',
            "★" * obj.rating + "☆" * (5 - obj.rating)
        )

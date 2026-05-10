from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

class AppointmentAdmin(ModelAdmin):
    list_display = ("full_name", "phone", "service", "preferred_date", "submitted_at", "is_read_badge", "action_buttons")
    list_display_links = ("full_name",)
    list_filter = ("is_read", "preferred_date", "service")
    search_fields = ("full_name", "phone")
    readonly_fields = ("full_name", "phone", "preferred_date", "preferred_time", "service", "message", "submitted_at")
    actions = ["mark_as_read"]
    fieldsets = (
        ("Patient Details", {"fields": ("full_name", "phone")}),
        ("Appointment Request", {"fields": ("preferred_date", "preferred_time", "service")}),
        ("Additional Info", {"fields": ("message", "submitted_at")}),
        ("Status", {"fields": ("is_read",)}),
    )

    class Media:
        js = ("ClinicAppStatic/admin_actions.js",)
        css = {"all": ("ClinicAppStatic/admin_actions.css",)}

    def action_buttons(self, obj):
        edit_url = reverse("admin:ClinicApp_appointment_change", args=[obj.pk])
        delete_url = reverse("admin:ClinicApp_appointment_delete", args=[obj.pk])

        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="action-btn action-btn--edit" title="View">'
            '<span class="material-symbols-outlined">visibility</span></a>'
            '<button type="button" class="action-btn action-btn--delete" '
            'title="Delete" onclick="adminDelete(\'{}\')">'
            '<span class="material-symbols-outlined">delete</span></button>'
            '</div>',
            edit_url, delete_url
        )

    action_buttons.short_description = "Actions"
    action_buttons.admin_order_field = None

    @display(description="Status")
    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html(
                '<span class="status-badge status-badge--read">✓ Read</span>'
            )
        return format_html(
            '<span class="status-badge status-badge--unread">● Unread</span>'
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

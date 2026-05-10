from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

class BaseAdmin(ModelAdmin):
    """Base admin with inline Edit/Delete buttons."""

    class Media:
        js = ("ClinicAppStatic/admin_preview.js", "ClinicAppStatic/admin_actions.js")
        css = {"all": ("ClinicAppStatic/admin_actions.css",)}

    def action_buttons(self, obj):
        opts = self.model._meta
        app_label = opts.app_label
        model_name = opts.model_name

        edit_url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk])
        delete_url = reverse(f"admin:{app_label}_{model_name}_delete", args=[obj.pk])

        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="action-btn action-btn--edit" title="Edit">'
            '<span class="material-symbols-outlined">edit</span></a>'
            '<button type="button" class="action-btn action-btn--delete" '
            'title="Delete" onclick="adminDelete(\'{}\')">'
            '<span class="material-symbols-outlined">delete</span></button>'
            '</div>',
            edit_url, delete_url
        )

    action_buttons.short_description = "Actions"
    action_buttons.admin_order_field = None

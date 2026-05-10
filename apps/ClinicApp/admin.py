"""
Dental Clinic - Admin Panel Configuration (Unfold Theme)

Registers all models with the Unfold-enhanced Django admin interface.
Each model includes inline Edit/Delete action buttons for quick management.
"""

from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import (
    HeroSection,
    Service,
    Doctor,
    Testimonial,
    GalleryImage,
    ClinicInfo,
    Appointment,
)

# Import custom admin site
from .admin_site import custom_site

# Unregister User model to hide from admin
from django.contrib.auth.models import User
try:
    custom_site.unregister(User)
except:
    pass


def get_unread_appointments_count(request: HttpRequest) -> str:
    count = Appointment.objects.filter(is_read=False).count()
    return str(count) if count > 0 else ""


def dashboard_callback(request: HttpRequest, context: dict) -> dict:
    context["total_appointments"] = Appointment.objects.count()
    context["unread_appointments"] = Appointment.objects.filter(is_read=False).count()
    context["total_doctors"] = Doctor.objects.count()
    context["total_services"] = Service.objects.count()
    context["recent_appointments"] = Appointment.objects.select_related("service").order_by("-submitted_at")[:5]
    return context


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

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    @admin.action(description="Mark selected appointments as Read")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} appointment(s) marked as read.")


# Register all models with custom_site
custom_site.register(HeroSection, HeroSectionAdmin)
custom_site.register(Service, ServiceAdmin)
custom_site.register(Doctor, DoctorAdmin)
custom_site.register(Testimonial, TestimonialAdmin)
custom_site.register(GalleryImage, GalleryImageAdmin)
custom_site.register(ClinicInfo, ClinicInfoAdmin)
custom_site.register(Appointment, AppointmentAdmin)

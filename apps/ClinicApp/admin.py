"""
Dental Clinic - Admin Panel Configuration (Unfold Theme)

Registers all models with the Unfold-enhanced Django admin interface.
Each model includes inline Edit/Delete action buttons for quick management.
Translation fields (RU, UZ, EN) are included in each model's fieldsets.
"""

from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import (
    HeroSection,
    Service,
    Doctor,
    Testimonial,
    GalleryImage,
    ClinicInfo,
    FAQ,
    Appointment,
)


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

    action_buttons.short_description = _("Actions")
    action_buttons.admin_order_field = None


@admin.register(HeroSection)
class HeroSectionAdmin(BaseAdmin):
    list_display = ("hero_header_display", "button_text", "is_active", "action_buttons")
    list_display_links = ("hero_header_display",)
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("headline", "subheadline", "button_text")
    fieldsets = (
        (_("Content — Russian (default)"), {"fields": ("headline_ru", "subheadline_ru")}),
        (_("Content — O'zbek"), {"fields": ("headline_uz", "subheadline_uz"), "classes": ("collapse",)}),
        (_("Content — English"), {"fields": ("headline_en", "subheadline_en"), "classes": ("collapse",)}),
        (_("Call to Action"), {"fields": ("button_text", "button_link")}),
        (_("Status"), {"fields": ("is_active",)}),
    )

    @display(description=_("Hero Section"), header=True)
    def hero_header_display(self, obj):
        sub = (obj.headline_ru or obj.headline_uz or obj.headline_en or "")[:80]
        sub += '...' if len(sub) > 80 else ""
        return [obj.headline_ru or obj.headline_uz or obj.headline_en, sub]


@admin.register(Service)
class ServiceAdmin(BaseAdmin):
    list_display = ("title", "icon_thumbnail", "order", "is_visible", "action_buttons")
    list_display_links = ("title",)
    list_editable = ("is_visible", "order")
    list_filter = ("is_visible",)
    search_fields = ("title_ru", "title_uz", "title_en", "description_ru")
    fieldsets = (
        (_("Service Details — Russian (default)"), {"fields": ("title_ru", "description_ru")}),
        (_("Service Details — O'zbek"), {"fields": ("title_uz", "description_uz"), "classes": ("collapse",)}),
        (_("Service Details — English"), {"fields": ("title_en", "description_en"), "classes": ("collapse",)}),
        (_("Media"), {"fields": ("icon_image",)}),
        (_("Display"), {"fields": ("order", "is_visible")}),
    )

    @display(description=_("Icon"))
    def icon_thumbnail(self, obj):
        if obj.icon_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:8px;object-fit:cover;" />',
                obj.icon_image.url
            )
        return "—"


@admin.register(Doctor)
class DoctorAdmin(BaseAdmin):
    list_display = ("photo_thumbnail", "full_name", "specialty", "experience_years", "order", "is_visible", "action_buttons")
    list_display_links = ("full_name",)
    list_editable = ("is_visible", "order")
    list_filter = ("is_visible", "specialty")
    search_fields = ("full_name_ru", "specialty_ru", "bio_ru")
    ordering = ("order",)
    fieldsets = (
        (_("Personal Info — Russian (default)"), {"fields": ("full_name_ru", "specialty_ru", "experience_years", "photo")}),
        (_("Personal Info — O'zbek"), {"fields": ("full_name_uz", "specialty_uz"), "classes": ("collapse",)}),
        (_("Personal Info — English"), {"fields": ("full_name_en", "specialty_en"), "classes": ("collapse",)}),
        (_("Biography — Russian (default)"), {"fields": ("bio_ru",)}),
        (_("Biography — O'zbek"), {"fields": ("bio_uz",), "classes": ("collapse",)}),
        (_("Biography — English"), {"fields": ("bio_en",), "classes": ("collapse",)}),
        (_("Display"), {"fields": ("order", "is_visible")}),
    )

    @display(description=_("Photo"))
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;object-fit:cover;" />',
                obj.photo.url
            )
        return "—"


@admin.register(Testimonial)
class TestimonialAdmin(BaseAdmin):
    list_display = ("patient_name", "rating_stars", "is_visible", "action_buttons")
    list_display_links = ("patient_name",)
    list_editable = ("is_visible",)
    list_filter = ("is_visible", "rating")
    search_fields = ("patient_name_ru", "review_text_ru")
    fieldsets = (
        (_("Patient Info — Russian (default)"), {"fields": ("patient_name_ru",)}),
        (_("Patient Info — O'zbek"), {"fields": ("patient_name_uz",), "classes": ("collapse",)}),
        (_("Patient Info — English"), {"fields": ("patient_name_en",), "classes": ("collapse",)}),
        (_("Review — Russian (default)"), {"fields": ("review_text_ru", "rating")}),
        (_("Review — O'zbek"), {"fields": ("review_text_uz",), "classes": ("collapse",)}),
        (_("Review — English"), {"fields": ("review_text_en",), "classes": ("collapse",)}),
        (_("Media"), {"fields": ("patient_photo",)}),
        (_("Status"), {"fields": ("is_visible",)}),
    )

    @display(description=_("Rating"))
    def rating_stars(self, obj):
        return format_html(
            '<span class="text-amber-400">{}</span>',
            "★" * obj.rating + "☆" * (5 - obj.rating)
        )


@admin.register(GalleryImage)
class GalleryImageAdmin(BaseAdmin):
    list_display = ("image_thumbnail", "caption", "order", "is_visible", "action_buttons")
    list_display_links = ("caption",)
    list_editable = ("order", "is_visible")
    list_filter = ("is_visible",)
    search_fields = ("caption_ru", "caption_uz", "caption_en")
    ordering = ("order",)
    fieldsets = (
        (_("Image Details"), {"fields": ("image",)}),
        (_("Caption — Russian (default)"), {"fields": ("caption_ru",)}),
        (_("Caption — O'zbek"), {"fields": ("caption_uz",), "classes": ("collapse",)}),
        (_("Caption — English"), {"fields": ("caption_en",), "classes": ("collapse",)}),
        (_("Display"), {"fields": ("order", "is_visible")}),
    )

    @display(description=_("Image"))
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="50" style="border-radius:8px;object-fit:cover;" />',
                obj.image.url
            )
        return "—"


@admin.register(ClinicInfo)
class ClinicInfoAdmin(BaseAdmin):
    list_display = ("clinic_name", "phone", "email", "logo_thumbnail", "action_buttons")
    list_display_links = ("clinic_name",)
    fieldsets = (
        (_("Basic Info — Russian (default)"), {"fields": ("clinic_name_ru", "address_ru", "phone", "working_hours_ru")}),
        (_("Basic Info — O'zbek"), {"fields": ("clinic_name_uz", "address_uz", "working_hours_uz"), "classes": ("collapse",)}),
        (_("Basic Info — English"), {"fields": ("clinic_name_en", "address_en", "working_hours_en"), "classes": ("collapse",)}),
        (_("Branding"), {"fields": ("logo",)}),
        (_("Social Media"), {"fields": ("facebook_url", "instagram_url", "youtube_url")}),
        (_("About Section — Russian (default)"), {"fields": ("about_text_ru", "about_image")}),
        (_("About Section — O'zbek"), {"fields": ("about_text_uz",), "classes": ("collapse",)}),
        (_("About Section — English"), {"fields": ("about_text_en",), "classes": ("collapse",)}),
        (_("Telegram Notifications"), {
            "classes": ("collapse",),
            "fields": ("telegram_bot_token", "telegram_chat_id"),
            "description": _("Enter your Telegram Bot Token (from @BotFather) and Group/Channel ID to receive appointment notifications."),
        }),
    )

    @display(description=_("Logo"))
    def logo_thumbnail(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="60" height="40" style="border-radius:8px;object-fit:contain;" />',
                obj.logo.url
            )
        return "—"

    def has_add_permission(self, request):
        return ClinicInfo.objects.count() < 1

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if ClinicInfo.objects.count() == 1:
            obj = ClinicInfo.objects.first()
            return redirect(reverse("admin:ClinicApp_clinicinfo_change", args=[obj.pk]))
        return super().changelist_view(request, extra_context)


@admin.register(FAQ)
class FAQAdmin(BaseAdmin):
    list_display = ("question", "order", "is_visible", "action_buttons")
    list_display_links = ("question",)
    list_editable = ("order", "is_visible")
    list_filter = ("is_visible",)
    search_fields = ("question_ru", "answer_ru")
    ordering = ("order",)
    fieldsets = (
        (_("Question — Russian (default)"), {"fields": ("question_ru",)}),
        (_("Question — O'zbek"), {"fields": ("question_uz",), "classes": ("collapse",)}),
        (_("Question — English"), {"fields": ("question_en",), "classes": ("collapse",)}),
        (_("Answer — Russian (default)"), {"fields": ("answer_ru",)}),
        (_("Answer — O'zbek"), {"fields": ("answer_uz",), "classes": ("collapse",)}),
        (_("Answer — English"), {"fields": ("answer_en",), "classes": ("collapse",)}),
        (_("Display"), {"fields": ("order", "is_visible")}),
    )


@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = ("full_name", "phone", "service", "preferred_date", "submitted_at", "is_read_badge", "action_buttons")
    list_display_links = ("full_name",)
    list_filter = ("is_read", "preferred_date", "service")
    search_fields = ("full_name", "phone", "email")
    readonly_fields = ("full_name", "phone", "email", "preferred_date", "preferred_time", "service", "message", "submitted_at")
    actions = ["mark_as_read"]
    fieldsets = (
        (_("Patient Details"), {"fields": ("full_name", "phone", "email")}),
        (_("Appointment Request"), {"fields": ("preferred_date", "preferred_time", "service")}),
        (_("Additional Info"), {"fields": ("message", "submitted_at")}),
        (_("Status"), {"fields": ("is_read",)}),
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

    action_buttons.short_description = _("Actions")
    action_buttons.admin_order_field = None

    @display(description=_("Status"))
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

    @admin.action(description=_("Mark selected appointments as Read"))
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, _(f"{updated} appointment(s) marked as read."))

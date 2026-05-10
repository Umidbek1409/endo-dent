from django.contrib import admin
from django.http import HttpRequest
from django.contrib.auth.models import User
from ..admin_site import custom_site
from ..models import (
    HeroSection,
    Service,
    Doctor,
    Testimonial,
    GalleryImage,
    ClinicInfo,
    Appointment,
)
from .admin import (
    HeroSectionAdmin,
    ServiceAdmin,
    DoctorAdmin,
    TestimonialAdmin,
    GalleryImageAdmin,
    ClinicInfoAdmin,
    AppointmentAdmin,
)

# Unregister User model from custom admin site
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

# Registration
custom_site.register(HeroSection, HeroSectionAdmin)
custom_site.register(Service, ServiceAdmin)
custom_site.register(Doctor, DoctorAdmin)
custom_site.register(Testimonial, TestimonialAdmin)
custom_site.register(GalleryImage, GalleryImageAdmin)
custom_site.register(ClinicInfo, ClinicInfoAdmin)
custom_site.register(Appointment, AppointmentAdmin)

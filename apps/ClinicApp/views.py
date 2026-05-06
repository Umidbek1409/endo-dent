"""
Dental Clinic - Views

This module contains view functions for the frontend and API endpoints.
- home(): Renders the main page with all dynamic content.
- submit_appointment(): Handles appointment form submissions via JSON API
  and sends notifications to Telegram.
"""

import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import (
    HeroSection,
    Service,
    Doctor,
    Testimonial,
    GalleryImage,
    ClinicInfo,
    Appointment,
)

logger = logging.getLogger(__name__)


def home(request):
    """
    Main homepage view.
    Queries all visible/active content from every model and passes it
    as context to the template for rendering.
    """
    clinic_info = ClinicInfo.objects.first()
    hero = HeroSection.objects.filter(is_active=True).first()
    services = Service.objects.filter(is_visible=True)
    doctors = Doctor.objects.filter(is_visible=True)
    testimonials = Testimonial.objects.filter(is_visible=True)
    gallery_images = GalleryImage.objects.filter(is_visible=True)

    context = {
        'clinic_info': clinic_info,
        'hero': hero,
        'services': services,
        'doctors': doctors,
        'testimonials': testimonials,
        'gallery_images': gallery_images,
    }
    return render(request, 'ClinicAppTemplates/index.html', context)


@csrf_exempt
@require_POST
def submit_appointment(request):
    """
    API endpoint to handle appointment form submissions.
    Accepts JSON POST data, validates required fields, saves to the database,
    and sends a notification to Telegram.
    Returns JSON response with success or error status.
    """
    try:
        data = json.loads(request.body)

        full_name = data.get('full_name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        preferred_date = data.get('preferred_date', '').strip()
        preferred_time = data.get('preferred_time', '').strip()
        service_id = data.get('service', None)
        message = data.get('message', '').strip()

        if not full_name:
            return JsonResponse({'success': False, 'error': 'Full name is required'})
        if not phone:
            return JsonResponse({'success': False, 'error': 'Phone number is required'})
        if not preferred_date:
            return JsonResponse({'success': False, 'error': 'Preferred date is required'})

        service_obj = None
        if service_id:
            try:
                service_obj = Service.objects.get(pk=service_id)
            except Service.DoesNotExist:
                service_obj = None

        appointment = Appointment.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            service=service_obj,
            message=message,
        )

        return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request data'})
    except Exception:
        logger.exception("Unexpected error in submit_appointment")
        return JsonResponse({'success': False, 'error': 'Internal server error'})

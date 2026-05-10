from django.shortcuts import render
from ..models import (
    HeroSection,
    Service,
    Doctor,
    Testimonial,
    GalleryImage,
    ClinicInfo,
)

def home(request):
    """
    Main homepage view.
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

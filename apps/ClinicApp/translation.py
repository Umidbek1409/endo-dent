"""
Translation configuration for django-modeltranslation.
Defines which model fields should be translatable into multiple languages.

Supported languages: Russian (default), Uzbek, English.
"""

from modeltranslation.translator import register, TranslationOptions

from .models import (
    HeroSection,
    Service,
    Doctor,
    Testimonial,
    GalleryImage,
    ClinicInfo,
    FAQ,
)


@register(HeroSection)
class HeroSectionTranslationOptions(TranslationOptions):
    fields = ('headline', 'subheadline', 'button_text')


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ('full_name', 'specialty', 'bio')


@register(Testimonial)
class TestimonialTranslationOptions(TranslationOptions):
    fields = ('patient_name', 'review_text')


@register(GalleryImage)
class GalleryImageTranslationOptions(TranslationOptions):
    fields = ('caption',)


@register(ClinicInfo)
class ClinicInfoTranslationOptions(TranslationOptions):
    fields = (
        'clinic_name',
        'address',
        'working_hours',
        'about_text',
    )


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')

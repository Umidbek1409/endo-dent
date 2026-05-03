"""
Dental Clinic - Database Models

This module defines all database models for the dental clinic website.
Each model represents an editable section of the site, enabling full
content management through the Django admin panel.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


# ─────────────────────────────────────────────
# HeroSection
# ─────────────────────────────────────────────
# Manages the top hero/banner section of the homepage.
# Only one hero section can be active at a time.
class HeroSection(models.Model):
    headline = models.CharField(
        max_length=200,
        help_text=_("Main headline text shown at the top of the homepage, e.g. 'Your Perfect Smile Starts Here'")
    )
    subheadline = models.TextField(
        help_text=_("Subtitle or description text displayed below the main headline")
    )
    background_image = models.ImageField(
        upload_to='hero/',
        help_text=_("Background image for the hero section. Recommended size: 1200x800px")
    )
    button_text = models.CharField(
        max_length=100,
        default="Book Appointment",
        help_text=_("Text displayed on the call-to-action button, e.g. 'Book Appointment'")
    )
    button_link = models.CharField(
        max_length=200,
        default="#",
        help_text=_("URL the button links to. Leave as '#' to open the booking modal")
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Check to display this hero section on the website. Uncheck to hide it.")
    )

    class Meta:
        verbose_name = _("Hero Section")
        verbose_name_plural = _("Hero Sections")

    def __str__(self):
        return self.headline


# ─────────────────────────────────────────────
# Service
# ─────────────────────────────────────────────
# Represents a dental service offered by the clinic.
# Displayed in the services grid on the homepage.
class Service(models.Model):
    title = models.CharField(
        max_length=150,
        help_text=_("Service name as it appears on the website, e.g. 'General Dentistry'")
    )
    description = models.TextField(
        help_text=_("Short description of the service shown on the service card")
    )
    icon_image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        help_text=_("Icon image for the service card. If left empty, a default tooth icon is shown.")
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text=_("Display order — lower numbers appear first on the website (e.g. 1, 2, 3)")
    )
    is_visible = models.BooleanField(
        default=True,
        help_text=_("Uncheck to hide this service from the website without deleting it")
    )

    class Meta:
        ordering = ['order']
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────
# Doctor
# ─────────────────────────────────────────────
# Represents a doctor/dentist on the clinic team.
# Displayed in the team section with photo and bio.
class Doctor(models.Model):
    full_name = models.CharField(
        max_length=150,
        help_text=_("Doctor's full name with title, e.g. 'Dr. James Wilson'")
    )
    specialty = models.CharField(
        max_length=150,
        help_text=_("Medical specialty, e.g. 'Lead Implantologist' or 'Orthodontics Specialist'")
    )
    bio = models.TextField(
        help_text=_("Short biography or description shown below the doctor's name")
    )
    photo = models.ImageField(
        upload_to='doctors/',
        help_text=_("Professional headshot photo of the doctor. Recommended: square image, at least 300x300px")
    )
    experience_years = models.PositiveIntegerField(
        help_text=_("Number of years of professional experience, e.g. 7")
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text=_("Display order — lower numbers appear first on the website (e.g. 1, 2, 3)")
    )
    is_visible = models.BooleanField(
        default=True,
        help_text=_("Uncheck to hide this doctor from the website without deleting the record")
    )

    class Meta:
        ordering = ['order']
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")

    def __str__(self):
        return self.full_name


# ─────────────────────────────────────────────
# Testimonial
# ─────────────────────────────────────────────
# Stores patient reviews and testimonials.
# Displayed in the testimonials section with star ratings.
class Testimonial(models.Model):
    # Rating choices from 1 to 5 stars
    RATING_CHOICES = [(i, f"{'⭐' * i} ({i}/5)") for i in range(1, 6)]

    patient_name = models.CharField(
        max_length=150,
        help_text=_("Patient's full name as shown in the review")
    )
    review_text = models.TextField(
        help_text=_("The patient's testimonial or review text")
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text=_("Star rating from 1 to 5 stars given by the patient")
    )
    patient_photo = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text=_("Optional photo of the patient. Leave empty if the patient prefers anonymity.")
    )
    is_visible = models.BooleanField(
        default=True,
        help_text=_("Uncheck to hide this testimonial from the website without deleting it")
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")

    def __str__(self):
        return f"{self.patient_name} - {'⭐' * self.rating}"


# ─────────────────────────────────────────────
# GalleryImage
# ─────────────────────────────────────────────
# Stores before/after or clinic photos for the gallery section.
class GalleryImage(models.Model):
    image = models.ImageField(
        upload_to='gallery/',
        help_text=_("Gallery image file. Recommended: landscape orientation, at least 600x400px")
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("Optional caption describing the image, e.g. 'Before & After: Teeth Whitening'")
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text=_("Display order — lower numbers appear first in the gallery grid (e.g. 1, 2, 3)")
    )
    is_visible = models.BooleanField(
        default=True,
        help_text=_("Uncheck to hide this image from the gallery without deleting it")
    )

    class Meta:
        ordering = ['order']
        verbose_name = _("Gallery Image")
        verbose_name_plural = _("Gallery Images")

    def __str__(self):
        return self.caption or f"Gallery Image #{self.id}"


# ─────────────────────────────────────────────
# ClinicInfo
# ─────────────────────────────────────────────
# Single-instance model holding general clinic information:
# contact details, social links, about text, and branding.
class ClinicInfo(models.Model):
    clinic_name = models.CharField(
        max_length=200,
        help_text=_("Official name of the clinic, e.g. 'BrightSmile Dental'")
    )
    address = models.TextField(
        help_text=_("Full physical address of the clinic, e.g. '123 Bright Avenue, Suite 200, New York, NY 10001'")
    )
    phone = models.CharField(
        max_length=50,
        help_text=_("Primary contact phone number, e.g. '(555) 123-4567'")
    )
    email = models.EmailField(
        help_text=_("Primary contact email address, e.g. 'hello@brightsmile.com'")
    )
    working_hours = models.TextField(
        help_text=_("Operating hours, e.g. 'Mon–Fri: 8AM–7PM | Sat: 9AM–4PM'")
    )
    logo = models.ImageField(
        upload_to='branding/',
        help_text=_("Clinic logo image displayed in the navigation bar and footer. Recommended: transparent PNG, 200x60px")
    )
    facebook_url = models.URLField(
        blank=True,
        default='',
        help_text=_("Full URL to the clinic's Facebook page. Leave empty to hide the Facebook link.")
    )
    instagram_url = models.URLField(
        blank=True,
        default='',
        help_text=_("Full URL to the clinic's Instagram page. Leave empty to hide the Instagram link.")
    )
    youtube_url = models.URLField(
        blank=True,
        default='',
        help_text=_("Full URL to the clinic's YouTube channel. Leave empty to hide the YouTube link.")
    )
    about_text = models.TextField(
        help_text=_("About section text describing the clinic's history, mission, and values")
    )
    about_image = models.ImageField(
        upload_to='about/',
        help_text=_("Image displayed in the About section. Recommended: 800x600px")
    )
    telegram_bot_token = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text=_("Telegram Bot Token from @BotFather, e.g. '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'")
    )
    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text=_("Telegram Group/Channel ID where notifications are sent, e.g. '-1001234567890'")
    )

    class Meta:
        verbose_name = _("Clinic Information")
        verbose_name_plural = _("Clinic Information")

    def __str__(self):
        return self.clinic_name

    def save(self, *args, **kwargs):
        """
        Override save to ensure only one ClinicInfo record exists.
        If one already exists, update it instead of creating a new one.
        """
        self.pk = 1  # Force primary key to 1 (singleton pattern)
        super().save(*args, **kwargs)


# ─────────────────────────────────────────────
# FAQ
# ─────────────────────────────────────────────
# Stores frequently asked questions and answers.
class FAQ(models.Model):
    question = models.CharField(
        max_length=300,
        help_text=_("The FAQ question text, e.g. 'Do you accept dental insurance?'")
    )
    answer = models.TextField(
        help_text=_("The detailed answer to the question")
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text=_("Display order — lower numbers appear first on the website (e.g. 1, 2, 3)")
    )
    is_visible = models.BooleanField(
        default=True,
        help_text=_("Uncheck to hide this FAQ from the website without deleting it")
    )

    class Meta:
        ordering = ['order']
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")

    def __str__(self):
        return self.question


# ─────────────────────────────────────────────
# Appointment
# ─────────────────────────────────────────────
# Stores appointment requests submitted through the website form.
# Each record represents one booking attempt.
class Appointment(models.Model):
    full_name = models.CharField(
        max_length=150,
        help_text=_("Patient's full name as entered in the booking form")
    )
    phone = models.CharField(
        max_length=50,
        help_text=_("Patient's phone number for callback confirmation")
    )
    email = models.EmailField(
        blank=True,
        default='',
        help_text=_("Patient's email address (optional)")
    )
    preferred_date = models.DateField(
        help_text=_("The date the patient requested for their appointment")
    )
    preferred_time = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text=_("The time the patient requested, e.g. '14:00' (optional)")
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("The dental service the patient selected when booking")
    )
    message = models.TextField(
        blank=True,
        default='',
        help_text=_("Any additional notes or comments the patient added")
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Automatically set — the date and time this appointment was submitted")
    )
    is_read = models.BooleanField(
        default=False,
        help_text=_("Check this box after you have reviewed the appointment request")
    )

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")

    def __str__(self):
        return f"{self.full_name} - {self.preferred_date}"

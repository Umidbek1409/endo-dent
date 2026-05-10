from django.db import models
from .service import Service

class Appointment(models.Model):
    full_name = models.CharField(
        max_length=150,
        help_text="Patient's full name as entered in the booking form"
    )
    phone = models.CharField(
        max_length=50,
        help_text="Patient's phone number for callback confirmation"
    )
    preferred_date = models.DateField(
        blank=True,
        null=True,
        help_text="The date the patient requested for their appointment (optional)"
    )
    preferred_time = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="The time the patient requested, e.g. '14:00' (optional)"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The dental service the patient selected when booking"
    )
    message = models.TextField(
        blank=True,
        default='',
        help_text="Any additional notes or comments the patient added"
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Automatically set — the date and time this appointment was submitted"
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Check this box after you have reviewed the appointment request"
    )

    class Meta:
        app_label = 'ClinicApp'
        ordering = ['-submitted_at']
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"{self.full_name} - {self.preferred_date}"

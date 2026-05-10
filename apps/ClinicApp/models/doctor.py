from django.db import models

class Doctor(models.Model):
    full_name = models.CharField(
        max_length=150,
        help_text="Doctor's full name with title, e.g. 'Dr. James Wilson'"
    )
    specialty = models.CharField(
        max_length=150,
        help_text="Medical specialty, e.g. 'Lead Implantologist' or 'Orthodontics Specialist'"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Short biography or description shown below the doctor's name (optional)"
    )
    photo = models.ImageField(
        upload_to='doctors/',
        blank=True,
        null=True,
        help_text="Professional headshot photo of the doctor. Recommended: square image, at least 300x300px. Leave empty for default avatar."
    )
    experience_years = models.PositiveIntegerField(
        help_text="Number of years of professional experience, e.g. 7"
    )
    order = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=0,
        help_text="Display order — lower numbers appear first on the website (e.g. 1, 2, 3) (optional)"
    )
    is_visible = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this doctor from the website without deleting the record"
    )

    class Meta:
        app_label = 'ClinicApp'
        ordering = ['order']
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return self.full_name

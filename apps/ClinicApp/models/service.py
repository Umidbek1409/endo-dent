from django.db import models

class Service(models.Model):
    title = models.CharField(
        max_length=150,
        help_text="Service name as it appears on the website, e.g. 'General Dentistry'"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Short description of the service shown on the service card (optional)"
    )
    icon_image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        help_text="Icon image for the service card. If left empty, a default tooth icon is shown."
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order — lower numbers appear first on the website (e.g. 1, 2, 3)"
    )
    is_visible = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this service from the website without deleting it"
    )

    class Meta:
        app_label = 'ClinicApp'
        ordering = ['order']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title

from django.db import models

class HeroSection(models.Model):
    headline = models.CharField(
        max_length=200,
        help_text="Main headline text shown at the top of the homepage, e.g. 'Your Perfect Smile Starts Here'"
    )
    subheadline = models.TextField(
        help_text="Subtitle or description text displayed below the main headline"
    )
    button_text = models.CharField(
        max_length=100,
        default="Book Appointment",
        help_text="Text displayed on the call-to-action button, e.g. 'Book Appointment'"
    )
    button_link = models.CharField(
        max_length=200,
        default="#",
        help_text="URL the button links to. Leave as '#' to open the booking modal"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Check to display this hero section on the website. Uncheck to hide it."
    )

    class Meta:
        app_label = 'ClinicApp'
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

from django.db import models

class ClinicInfo(models.Model):
    clinic_name = models.CharField(
        max_length=200,
        help_text="Official name of the clinic, e.g. 'BrightSmile Dental'"
    )
    address = models.TextField(
        help_text="Full physical address of the clinic, e.g. '123 Bright Avenue, Suite 200, New York, NY 10001'"
    )
    phone = models.CharField(
        max_length=50,
        help_text="Primary contact phone number, e.g. '(555) 123-4567'"
    )
    email = models.EmailField(
        help_text="Primary contact email address, e.g. 'hello@brightsmile.com'"
    )
    working_hours = models.TextField(
        help_text="Operating hours, e.g. 'Mon–Fri: 8AM–7PM | Sat: 9AM–4PM'"
    )
    instagram_url = models.URLField(
        blank=True,
        default='',
        help_text="Full URL to the clinic's Instagram page. Leave empty to hide the Instagram link."
    )
    telegram_url = models.URLField(
        blank=True,
        default='',
        help_text="Full URL to the clinic's Telegram channel. Leave empty to hide the Telegram link."
    )
    telegram_bot_token = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text="Telegram Bot Token from @BotFather, e.g. '123456789:ABCdefGHIjklMNOpqrsTUVwxyz'"
    )
    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="Your personal Telegram Chat ID to receive appointment notifications. Get it from @userinfobot"
    )
    about_text = models.TextField(
        help_text="About section text describing the clinic's history, mission, and values"
    )
    about_image = models.ImageField(
        upload_to='about/',
        blank=True,
        null=True,
        help_text="Image displayed in the About section. Recommended: 800x600px. Leave empty for gradient placeholder."
    )

    class Meta:
        app_label = 'ClinicApp'
        verbose_name = "Clinic Information"
        verbose_name_plural = "Clinic Information"

    def __str__(self):
        return self.clinic_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

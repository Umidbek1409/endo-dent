from django.db import models

class Testimonial(models.Model):
    RATING_CHOICES = [(i, f"{'⭐' * i} ({i}/5)") for i in range(1, 6)]

    patient_name = models.CharField(
        max_length=150,
        help_text="Patient's full name as shown in the review"
    )
    review_text = models.TextField(
        help_text="The patient's testimonial or review text"
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="Star rating from 1 to 5 stars given by the patient"
    )
    patient_photo = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text="Optional photo of the patient. Leave empty if the patient prefers anonymity."
    )
    is_visible = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this testimonial from the website without deleting it"
    )

    class Meta:
        app_label = 'ClinicApp'
        ordering = ['-id']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.patient_name} - {'⭐' * self.rating}"

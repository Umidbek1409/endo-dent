from django.db import models

class GalleryImage(models.Model):
    image = models.ImageField(
        upload_to='gallery/',
        blank=True,
        null=True,
        help_text="Gallery image file. Recommended: landscape orientation, at least 600x400px. Leave empty for placeholder."
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional caption describing the image, e.g. 'Before & After: Teeth Whitening'"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order — lower numbers appear first in the gallery grid (e.g. 1, 2, 3)"
    )
    is_visible = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this image from the gallery without deleting it"
    )

    class Meta:
        app_label = 'ClinicApp'
        ordering = ['order']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.caption or f"Gallery Image #{self.id}"

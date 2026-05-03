"""
Dental Clinic Project - Root URL Configuration

Defines the main URL routing for the entire Django project:
- 'admin/': Unfold-enhanced Django admin panel for content management.
- '' (root): Includes all URL patterns from the ClinicApp.
- Media files are served from /media/ during development.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Unfold admin panel: accessible at /admin/
    path('admin/', admin.site.urls),
    # Include all URL patterns from the ClinicApp at the root path
    path('', include('apps.ClinicApp.urls')),
]

# Serve uploaded media files during development (DEBUG=True only).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
Dental Clinic Project - Root URL Configuration

Defines the main URL routing for the entire Django project:
- 'admin/': Unfold-enhanced Django admin panel for content management.
- '' (root): Includes all URL patterns from the ClinicApp.
- Media files are served from /media/ in both development and production.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.static import serve

from apps.ClinicApp.admin_site import custom_site

urlpatterns = [
    # Unfold-enhaced Django admin panel: accessible at /admin/
    path('admin/', custom_site.urls),
    # Include all URL patterns from the ClinicApp at the root path
    path('', include('apps.ClinicApp.urls')),
]

# Serve uploaded media files in both development and production.
if settings.DEBUG:
    # Use Django's built-in static serving for development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Use Django's static serve view for production (works without DEBUG)
    urlpatterns += [
        re_path(r'^media/(?P<path>.+)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

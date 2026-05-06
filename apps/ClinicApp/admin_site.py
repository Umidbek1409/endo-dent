"""
Custom admin site to disable password change and remove Users completely.
"""
from unfold.sites import UnfoldAdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import path, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import admin


class CustomAdminSite(UnfoldAdminSite):
    default_site = "admin"
    
    def __init__(self, name='admin'):
        super().__init__(name)
        # Unregister User to hide from admin
        try:
            self.unregister(User)
        except:
            pass
    
    def password_change(self, request, extra_context=None):
        # Disable password change by redirecting to admin home
        return HttpResponseRedirect('/admin/')
    
    def get_urls(self):
        # Get default URLs
        urlpatterns = super().get_urls()
        # Filter out any URL with 'password_change' in name
        filtered_urls = []
        for url in urlpatterns:
            if hasattr(url, 'name') and 'password_change' in str(url.name):
                continue
            filtered_urls.append(url)
        return filtered_urls
    
    def get_sidebar_navigation(self, request, context):
        # Get default navigation
        nav = super().get_sidebar_navigation(request, context)
        # Remove any 'Users' items from navigation
        if isinstance(nav, list):
            nav = [item for item in nav if 'Users' not in str(item.get('title', ''))]
        return nav


# Create custom admin site instance
# First unregister User from default admin
try:
    admin.site.unregister(User)
except:
    pass

custom_site = CustomAdminSite(name='admin')

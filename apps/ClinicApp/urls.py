"""
Dental Clinic App - URL Configuration

Defines URL patterns for the clinic app:
- '' (root): Renders the homepage with all dynamic content.
- 'api/appointment/': POST endpoint for submitting appointment forms.
"""

from django.urls import path

from . import views

urlpatterns = [
    # Homepage: renders the main page with all dynamic content from the database
    path('', views.home, name='home'),
    # Appointment API: accepts POST requests to create new appointment records
    path('api/appointment/', views.submit_appointment, name='submit_appointment'),
]

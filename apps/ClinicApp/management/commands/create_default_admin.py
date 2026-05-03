"""
Django management command to automatically create a superuser
if one does not already exist. Uses environment variables for credentials.

Usage:
    python manage.py create_default_admin

Environment variables:
    ADMIN_USERNAME - Admin username (default: 'admin')
    ADMIN_EMAIL    - Admin email (default: 'admin@example.com')
    ADMIN_PASSWORD - Admin password (REQUIRED if creating new user)
"""

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates a default superuser if none exists"

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS("Superuser already exists. Skipping."))
            return

        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        password = os.environ.get("ADMIN_PASSWORD")

        if not password:
            self.stdout.write(self.style.WARNING(
                "ADMIN_PASSWORD not set. No superuser created. "
                "Set the ADMIN_PASSWORD environment variable to create one."
            ))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS(
            f"Superuser '{username}' created successfully!"
        ))

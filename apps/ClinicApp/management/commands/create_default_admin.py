"""
Django management command to automatically create or update a superuser
using environment variables. This ensures admin credentials are always
correct on every deploy.

Usage:
    python manage.py create_default_admin

Environment variables:
    ADMIN_USERNAME - Admin username (default: 'admin')
    ADMIN_EMAIL    - Admin email (default: 'admin@example.com')
    ADMIN_PASSWORD - Admin password (REQUIRED)
"""

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates or updates the default superuser"

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        password = os.environ.get("ADMIN_PASSWORD")

        if not password:
            self.stdout.write(self.style.ERROR(
                "ADMIN_PASSWORD environment variable is required."
            ))
            return

        user = User.objects.filter(username=username).first()

        if user:
            user.set_password(password)
            user.email = email
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f"Superuser '{username}' updated successfully!"
            ))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS(
                f"Superuser '{username}' created successfully!"
            ))

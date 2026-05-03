"""
Dental Clinic - Django Settings
This file configures all aspects of the Django project including database,
static files, media uploads, security, and app registration.
Environment variables are loaded from .env file using django-environ.
"""

import os
from pathlib import Path

import environ
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize django-environ to read .env file from the project root
env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, ''),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ─────────────────────────────────────────────
# CORE SETTINGS
# ─────────────────────────────────────────────

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# ─────────────────────────────────────────────
# APPLICATION DEFINITION
# ─────────────────────────────────────────────

# All installed Django apps and third-party packages.
# UNFOLD: Must come BEFORE django.contrib.admin to override the default admin templates.
# unfold.contrib.filters: Provides advanced filter functionality in admin list views.
# unfold.contrib.forms: Provides enhanced form widgets for the admin panel.
# Built-in contrib apps provide admin, auth, sessions, etc.
# 'apps.ClinicApp' is our custom app containing models, views, and templates.
INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'apps.ClinicApp',
]

# ─────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration module
ROOT_URLCONF = 'config.DentalClinicConfig.urls'

# ─────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────

# Configuration for Django's template engine.
# APP_DIRS=True means Django will look for templates in each app's templates/ folder.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'apps' / 'ClinicApp' / 'templates',  # Custom admin overrides (must be before app dirs)
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Adds request object to templates
                'django.template.context_processors.i18n',  # Adds language context to templates
                'django.contrib.auth.context_processors.auth', # Adds user object to templates
                'django.contrib.messages.context_processors.messages',  # Adds messages to templates
            ],
        },
    },
]

# WSGI application entry point for serving the project
WSGI_APPLICATION = 'config.DentalClinicConfig.wsgi.application'

# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────

# SQLite database for development. Replace with PostgreSQL in production.
# db.sqlite3 file will be created in the project root.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─────────────────────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────────────────────

# Validators that enforce password strength requirements for user accounts.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ─────────────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────────────

# Default language code for the site
LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('ru', 'Русский'),
    ('uz', "O'zbek"),
    ('en', 'English'),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('ru',),
}

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

# ─────────────────────────────────────────────
# STATIC FILES (CSS, JavaScript, Images)
# ─────────────────────────────────────────────

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'apps' / 'ClinicApp' / 'static',
]

# WhiteNoise for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─────────────────────────────────────────────
# MEDIA FILES (User-uploaded images)
# ─────────────────────────────────────────────

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─────────────────────────────────────────────
# DEFAULT FIELD TYPES
# ─────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─────────────────────────────────────────────
# PRODUCTION SECURITY
# ─────────────────────────────────────────────

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ─────────────────────────────────────────────
# UNFOLD ADMIN THEME CONFIGURATION
# ─────────────────────────────────────────────

# UNFOLD replaces the default Django admin with a modern, responsive interface.
# This configuration controls the sidebar, branding, colors, and navigation.
UNFOLD = {
    # ── Branding ──────────────────────────
    "SITE_TITLE": "PearlSmile Admin",
    "SITE_HEADER": "PearlSmile Dental Clinic",
    "SITE_LOGO": lambda request: staticfiles_storage.url("ClinicAppStatic/logo.svg"),
    "SITE_LOGO_DARK": lambda request: staticfiles_storage.url("ClinicAppStatic/logo.svg"),
    "SITE_FAVICON": lambda request: staticfiles_storage.url("ClinicAppStatic/favicon.ico"),

    # ── Styles ────────────────────────────
    "STYLES": [
        lambda request: staticfiles_storage.url("ClinicAppStatic/admin_actions.css"),
    ],

    # ── Color Theme ───────────────────────
    "COLORS": {
        "primary": {
            "50":  "240 249 255",
            "100": "224 242 254",
            "200": "186 230 253",
            "300": "125 211 252",
            "400": "56  189 248",
            "500": "14  165 233",
            "600": "2   132 199",
            "700": "3   105 161",
            "800": "7   89  133",
            "900": "12  74  110",
            "950": "8   47  73",
        },
    },

    # ── Dashboard Callback ────────────────
    "DASHBOARD_CALLBACK": "apps.ClinicApp.admin.dashboard_callback",

    # ── Language Switcher ─────────────────
    # "SHOW_LANGUAGES": True,

    # ── Sidebar Navigation ────────────────
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            # ── Website Content group ──
            {
                "title": "Website Content",
                "separator": True,
                "items": [
                    {
                        "title": "Hero Section",
                        "icon": "image",
                        "link": reverse_lazy("admin:ClinicApp_herosection_changelist"),
                    },
                    {
                        "title": "About & Clinic Info",
                        "icon": "info",
                        "link": reverse_lazy("admin:ClinicApp_clinicinfo_changelist"),
                    },
                    {
                        "title": "Services",
                        "icon": "medical_services",
                        "link": reverse_lazy("admin:ClinicApp_service_changelist"),
                    },
                    {
                        "title": "Our Doctors",
                        "icon": "stethoscope",
                        "link": reverse_lazy("admin:ClinicApp_doctor_changelist"),
                    },
                    {
                        "title": "Gallery",
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:ClinicApp_galleryimage_changelist"),
                    },
                    {
                        "title": "Patient Reviews",
                        "icon": "star",
                        "link": reverse_lazy("admin:ClinicApp_testimonial_changelist"),
                    },
                    {
                        "title": "FAQ",
                        "icon": "help",
                        "link": reverse_lazy("admin:ClinicApp_faq_changelist"),
                    },
                ],
            },
            # ── Appointments group ──
            {
                "title": "Appointments",
                "separator": True,
                "items": [
                    {
                        "title": "All Appointments",
                        "icon": "calendar_month",
                        "link": reverse_lazy("admin:ClinicApp_appointment_changelist"),
                        "badge": "apps.ClinicApp.admin.get_unread_appointments_count",
                        "badge_variant": "warning",
                    },
                ],
            },
            # ── System group ──
            {
                "title": "System",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
        ],
    },
}

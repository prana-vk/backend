"""
Django settings for giyatra_project.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ------------------------------------------------------------
# BASE CONFIGURATION
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-y0ur-s3cr3t-k3y-h3r3-ch@ng3-1n-pr0duct10n"
)

DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Allowed hosts
ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    "backend-k4x8.onrender.com,localhost,127.0.0.1"
).split(",")

# Allow all subdomains of onrender.com in production
if not DEBUG:
    ALLOWED_HOSTS.append(".onrender.com")

# ------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------
INSTALLED_APPS = [
    # Default Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "corsheaders",

    # Local apps
    "home",
    "adver",
    "itinerary",
    "admin_panel",
]

# ------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For static file handling
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "giyatra_project.urls"

# ------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "giyatra_project.wsgi.application"

# ------------------------------------------------------------
# DATABASE CONFIGURATION (PostgreSQL only)
# ------------------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
        default="postgres://postgres:password@localhost:5432/giyatra_db"
    )
}

# ------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# ------------------------------------------------------------
# STATIC & MEDIA FILES
# ------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise configuration
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Use persistent disk on Render if available
if os.environ.get("RENDER") == "true" or os.path.exists("/opt/render/project/src/media"):
    MEDIA_ROOT = "/opt/render/project/src/media"
else:
    MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# ------------------------------------------------------------
# SITE URL (for absolute image URLs)
# ------------------------------------------------------------
SITE_URL = os.environ.get("SITE_URL", "https://backend-k4x8.onrender.com")

# ------------------------------------------------------------
# REST FRAMEWORK SETTINGS
# ------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# ------------------------------------------------------------
# CORS CONFIGURATION
# ------------------------------------------------------------
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "https://backend-k4x8.onrender.com,http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
).split(",")

CORS_ALLOW_CREDENTIALS = True

# ------------------------------------------------------------
# ADMIN PANEL CONFIGURATION (Set via environment)
# ------------------------------------------------------------
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# ------------------------------------------------------------
# DEFAULT AUTO FIELD
# ------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

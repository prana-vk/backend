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
    "rest_framework.authtoken",
    "corsheaders",

    # Local apps
    "home",
    "adver",
    "itinerary",
    "admin_panel",
    # Local accounts app (provides auth endpoints and models)
    "accounts",
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

# FRONTEND URL used for building links (password reset pages etc.)
FRONTEND_URL = os.environ.get('FRONTEND_URL', os.environ.get('SITE_URL', 'https://gi-yatra-frontend.vercel.app'))

# API key that the frontend may use when calling certain auth endpoints (optional)
FRONTEND_API_KEY = os.environ.get('FRONTEND_API_KEY', '')

# ------------------------------------------------------------
# EMAIL / SMTP SETTINGS (read from environment)
# ------------------------------------------------------------
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', None)
if not EMAIL_BACKEND:
    # default to SMTP backend in production, console backend in DEBUG for convenience
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587') or 587)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False').lower() == 'true'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'no-reply@example.com')

# ------------------------------------------------------------
# REST FRAMEWORK SETTINGS
# ------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "5/minute",
        "user": "20/minute",
        "signup_otp": "3/minute",
        "password_reset_otp": "3/minute",
    },
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
# CSRF / HTTPS related settings
# - Provide a configurable CSRF_TRUSTED_ORIGINS list and sensible
#   cookie SameSite defaults for local HTTPS testing (mkcert/ngrok)
# ------------------------------------------------------------
# Allow explicit override via environment variable (comma-separated, include scheme)
raw_csrf_trusted = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if raw_csrf_trusted:
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in raw_csrf_trusted.split(',') if u.strip()]
else:
    # derive trusted origins from HTTPS entries in CORS_ALLOWED_ORIGINS
    CSRF_TRUSTED_ORIGINS = [u for u in CORS_ALLOWED_ORIGINS if u.startswith('https://')]
    # ensure SITE_URL and FRONTEND_URL are included when they are HTTPS
    try:
        if SITE_URL and SITE_URL.startswith('https://') and SITE_URL not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(SITE_URL)
    except NameError:
        pass
    try:
        if FRONTEND_URL and FRONTEND_URL.startswith('https://') and FRONTEND_URL not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(FRONTEND_URL)
    except NameError:
        pass

# Support proxies that set X-Forwarded-Proto (useful for ngrok or local proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie SameSite settings: when running with secure cookies (HTTPS), it is
# often necessary to set SameSite=None for cross-site frontend (SPA) cookies.
if not DEBUG:
    # Default to None so browsers allow cross-site cookies when frontend is on another origin
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'None')
    CSRF_COOKIE_SAMESITE = os.environ.get('CSRF_COOKIE_SAMESITE', 'None')
else:
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'

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


# ------------------------------------------------------------
# PRODUCTION SECURITY SETTINGS
# These are enabled when DEBUG is False. Values can be overridden
# via environment variables for fine-grained control on the host.
# ------------------------------------------------------------
if not DEBUG:
    # HTTP Strict Transport Security (HSTS)
    # Default to 1 year; set to a shorter value if you want to test first.
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get(
        "SECURE_HSTS_INCLUDE_SUBDOMAINS", "True"
    ).lower() == "true"
    SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "True").lower() == "true"

    # Redirect all non-HTTPS requests to HTTPS
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() == "true"

    # Make session and CSRF cookies secure (sent only over HTTPS)
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "True").lower() == "true"
    CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "True").lower() == "true"

    # Additional recommended security headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = os.environ.get("X_FRAME_OPTIONS", "DENY")
else:
    # In debug/development keep these False to avoid interfering with local workflows
    SECURE_HSTS_SECONDS = 0
    SECURE_SSL_REDIRECT = False
    # Allow cookies over both HTTP and HTTPS in dev
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# ------------------------------------------------------------
# Additional production-hardening defaults and runtime checks
# ------------------------------------------------------------
# HTTP-only for session cookie; CSRF cookie must be readable by JS for SPA CSRF flow
SESSION_COOKIE_HTTPONLY = True
# CSRF cookie must NOT be HttpOnly because frontend JS reads it to set X-CSRFToken
CSRF_COOKIE_HTTPONLY = False

# Strict referrer policy for improved privacy/security
SECURE_REFERRER_POLICY = os.environ.get('SECURE_REFERRER_POLICY', 'strict-origin-when-cross-origin')

from django.core.exceptions import ImproperlyConfigured

def _production_sanity_checks():
    """Raise helpful errors if running with insecure settings in production."""
    if DEBUG:
        return
    # SECRET_KEY must not be the insecure default
    if (not SECRET_KEY) or SECRET_KEY.startswith('django-insecure') or 'go-insecure' in SECRET_KEY:
        raise ImproperlyConfigured("In production DEBUG=False, please set a strong SECRET_KEY in the environment.")

    # ALLOWED_HOSTS should not be empty or contain a wildcard in production
    if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
        raise ImproperlyConfigured("ALLOWED_HOSTS must be set to the production host(s) when DEBUG=False.")

    # Ensure secure cookie flags and SSL redirect are enabled in production
    if not SECURE_SSL_REDIRECT:
        raise ImproperlyConfigured("SECURE_SSL_REDIRECT should be True in production to force HTTPS.")
    if not SESSION_COOKIE_SECURE or not CSRF_COOKIE_SECURE:
        raise ImproperlyConfigured("SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE should be True in production.")


# Run sanity checks immediately so mistakes are visible early when starting the app
try:
    _production_sanity_checks()
except ImproperlyConfigured:
    # Re-raise so startup fails clearly in deploys; during development DEBUG=True so this won't run
    raise

# ---
# Note: For local dev, SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE are False so cookies work over HTTP.
# In production, these are True so cookies are only sent over HTTPS.
# ---

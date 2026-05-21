"""
Production settings — imports from base settings then overrides.
Usage: DJANGO_SETTINGS_MODULE=nomadsocks.settings_prod
"""

import os

from .settings import *  # noqa

DEBUG = False

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")

# Database — PostgreSQL
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(default=os.environ.get("DATABASE_URL")),
}

# Static files
STATIC_ROOT = BASE_DIR / "staticfiles"
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

# CORS — restrict to your domain
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    os.environ.get("FRONTEND_URL", "https://yourdomain.com"),
]

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# Payment provider credentials
QPAY_USERNAME = os.environ.get("QPAY_USERNAME", "")
QPAY_PASSWORD = os.environ.get("QPAY_PASSWORD", "")
QPAY_INVOICE_CODE = os.environ.get("QPAY_INVOICE_CODE", "")
SOCIALPAY_APP_ID = os.environ.get("SOCIALPAY_APP_ID", "")
SOCIALPAY_SECRET = os.environ.get("SOCIALPAY_SECRET", "")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")

BACKEND_URL = os.environ.get("BACKEND_URL", "")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "")

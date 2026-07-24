"""
Django settings for URL Shortener project.
"""

import os
from datetime import timedelta
from pathlib import Path
from decouple import config, Csv
from dotenv import load_dotenv

# ============================================================================
# 1. ENVIRONMENT SETUP
# ============================================================================

# Load variables from .env file into the operating system's environment.
# This lets us use os.getenv() anywhere in this file.
load_dotenv()

# Build paths inside the project like BASE_DIR / 'subdir'.
# __file__ is this file (settings.py). .parent.parent goes up two levels:
# config/ -> url_shortner/
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# 2. CORE SECURITY SETTINGS
# ============================================================================

# SECRET_KEY is used for cryptographic signing (sessions, passwords, CSRF).
# We pull it from the environment so it never lives in source code.
SECRET_KEY = os.getenv('SECRET_KEY')

# DEBUG mode shows detailed error pages. NEVER leave True in production.
# os.getenv returns a string, so we convert to boolean.
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Which hosts/IPs can serve this Django site.
# We parse the comma-separated string from .env into a Python list.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# ============================================================================
# 3. APPLICATION DEFINITION
# ============================================================================

# We split apps into three groups for readability:
#   - Django built-in apps (admin, auth, sessions, etc.)
#   - Third-party libraries (DRF, JWT, Swagger)
#   - Our custom apps (accounts, urls)

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',                     # Django REST Framework
    'rest_framework_simplejwt',           # JWT authentication
    'drf_spectacular',                    # OpenAPI 3 / Swagger generation
]

LOCAL_APPS = [
    'accounts',                           # Our user authentication app
    'urls',                               # Our URL shortener app
]

# Django merges all three lists into one registry.
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware is a stack of "hooks" that process requests and responses.
# Order matters: SecurityMiddleware runs first, then Session, then Auth, etc.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Tells Django where to find the root URLconf (routing table).
ROOT_URLCONF = 'config.urls'

# Template engine configuration. DRF uses JSON, but admin and browsable API need HTML.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],                       # Custom template folders (none yet)
        'APP_DIRS': True,                 # Look inside each app's templates/ folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Entry point for WSGI-compatible web servers (Gunicorn in production).
WSGI_APPLICATION = 'config.wsgi.application'

# Try DATABASE_URL first (Render sets this), fallback to individual vars
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }

# ============================================================================
# 5. PASSWORD VALIDATION
# ============================================================================

# Django's built-in password strength rules. These run when users register.
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

# ============================================================================
# 6. INTERNATIONALIZATION & STATIC FILES
# ============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True                 # Use timezone-aware datetimes (best practice)

# URL to serve static files (CSS, JS) from. Used by admin and browsable API.
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key type. 'BigAutoField' is 64-bit (supports more rows).
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# 7. DJANGO REST FRAMEWORK CONFIGURATION
# ============================================================================

REST_FRAMEWORK = {
    # Every request must authenticate via JWT by default.
    # We will explicitly override this to "AllowAny" on public endpoints
    # (registration, login, redirect) in their specific views.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # Default permission: AllowAny for now so we can test Swagger easily.
    # In production, many teams flip this to IsAuthenticated and explicitly
    # open up individual views. We will secure our views explicitly later.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

    # Tells DRF to use drf-spectacular for automatic schema generation.
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ============================================================================
# 8. SIMPLE JWT SETTINGS
# ============================================================================

SIMPLE_JWT = {
    # How long an access token lasts before the user must refresh it.
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),

    # How long a refresh token lasts. After this, the user must log in again.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# ============================================================================
# 9. DRF-SPECTACULAR (SWAGGER) SETTINGS
# ============================================================================

SPECTACULAR_SETTINGS = {
    'TITLE': 'URL Shortener API',
    'DESCRIPTION': 'A production-quality URL shortener API built with Django REST Framework.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,   # Don't bundle raw schema JSON at /api/schema/
}

import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://matchpointfront.vercel.app",
    "https://bookish-space-carnival-v46qwgxr799fp64g-8000.app.github.dev",
    "http://ec2-44-201-157-94.compute-1.amazonaws.com",
    "https://api.matchpoint.ma"
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://matchpointfront.vercel.app",
    "https://bookish-space-carnival-v46qwgxr799fp64g-8000.app.github.dev",
    "http://ec2-44-201-157-94.compute-1.amazonaws.com",
    "https://api.matchpoint.ma"
]

CORS_ALLOW_CREDENTIALS = True

APPEND_SLASH = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.DisableCSRFMiddleware',  # Middleware pour désactiver CSRF pour les API
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'channels',
    'core',
]

# Configuration Channels
ASGI_APPLICATION = 'matchpoint_backend.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# ── 11. Autres
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


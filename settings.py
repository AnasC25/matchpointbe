import os
from dotenv import load_dotenv
from pathlib import Path
from corsheaders.defaults import default_headers

# ───── Chemins & .env ─────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ───── Hôtes autorisés ─────
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ───── CORS (Cross-Origin Resource Sharing) ─────
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://matchpoint-beta.vercel.app",
    "http://matchpoint-beta.vercel.app",
    "http://ec2-44-201-157-94.compute-1.amazonaws.com",
    "https://api.matchpoint.ma",
    "https://appli.matchpoint.ma"
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'authorization',
    'content-type',
]

# ───── CSRF ─────
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://matchpoint-beta.vercel.app",
    "http://ec2-44-201-157-94.compute-1.amazonaws.com",
    "https://api.matchpoint.ma",
    "https://appli.matchpoint.ma"
]

# ───── Middleware ─────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Désactive temporairement CSRF si API pure
    'core.middleware.DisableCSRFMiddleware',
]

# ───── Applications installées ─────
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'channels',
    'core',
]

# ───── REST Framework ─────
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

# ───── Channels (WebSockets) ─────
ASGI_APPLICATION = 'matchpoint_backend.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# ───── Options diverses ─────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = True

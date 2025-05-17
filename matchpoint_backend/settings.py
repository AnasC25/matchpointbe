import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# ✅ Utilisation de CustomUser comme modèle utilisateur
AUTH_USER_MODEL = 'core.CustomUser'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://api.matchpoint.ma",
    "https://matchpointfront.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# ── 1. Chemin vers la racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# ── 2. Chargement du .env
load_dotenv(BASE_DIR / '.env')

# ── 3. Secret key et debug depuis l'env
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-dev-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Configuration CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://api.matchpoint.ma",
    "https://matchpointfront.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# ── 4. Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'core',
]

# ── 5. Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'core.middleware.DisableCSRFMiddleware',  # Middleware personnalisé pour désactiver CSRF pour les API
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'matchpoint_backend.urls'

# ── 6. Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'matchpoint_backend.wsgi.application'

# ── 7. Django REST Framework & JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':      timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME':     timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':      True,
    'BLACKLIST_AFTER_ROTATION':   True,
    'ALGORITHM':                  'HS256',
    'SIGNING_KEY':                os.getenv('JWT_SIGNING_KEY', 'your-dev-key'),
    'AUTH_HEADER_TYPES':          ('Bearer',),
    'USER_ID_FIELD':              'id',
    'USER_ID_CLAIM':              'user_id',
}

# ── 8. Base de données
load_dotenv()  # Charge les variables depuis .env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ── 9. Internationalisation
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ── 10. Static & Media
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── 11. Autres
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = False
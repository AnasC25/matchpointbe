from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

# ✅ Utilisation de CustomUser comme modèle utilisateur
AUTH_USER_MODEL = 'core.CustomUser'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://matchpoint-beta.vercel.app/",
    "https://api.matchpoint.ma",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# ── 1. Chemin vers la racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# ── 2. Chargement du .env
load_dotenv(BASE_DIR / '.env')

# ── 3. Secret key et debug depuis l'env
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

# Configuration CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://matchpoint-beta.vercel.app/',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
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
    'channels',
    'core',
]

# ── 5. Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.DisableCSRFMiddleware',  # Middleware personnalisé pour désactiver CSRF pour les API
]

ROOT_URLCONF = 'matchpoint_backend.urls'

# ── 6. Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
ASGI_APPLICATION = 'matchpoint_backend.asgi.application'

# ── 7. Django REST Framework & JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
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
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# ── 9. Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Casablanca'
USE_I18N = True
USE_TZ = True

# ── 10. Static & Media
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ── 11. Autres
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = True

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

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
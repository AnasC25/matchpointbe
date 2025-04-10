import os
from pathlib import Path
from datetime import timedelta

# ✅ Utilisation de CustomUser comme modèle utilisateur
AUTH_USER_MODEL = 'core.CustomUser'

# ✅ Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Clé secrète (change-la en production)
SECRET_KEY = 'django-insecure-*i#-e*kz!+2+kzi96hdo1jvchyspqhw9ezjx2xqrhcd7jk8#fv'

# ✅ Mode Debug (⚠️ Mettre False en production)
DEBUG = True

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True  # Éviter les erreurs CORS avec les cookies

# ✅ Configuration des hôtes autorisés (à modifier en production)
ALLOWED_HOSTS = []

# ✅ Applications installées
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
    'corsheaders',  # Ajout pour la gestion des CORS
    'core',
]

# ✅ Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Doit être placé en haut
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ Fichier principal des URLs du projet
ROOT_URLCONF = 'matchpoint_backend.urls'

# ✅ Configuration des templates (nécessaire pour Django Admin)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Ajoute des répertoires si besoin
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

# ✅ Django REST Framework & JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'your-secret-key',  # Change-moi en production
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',  # Assure que JWT récupère bien l'ID utilisateur
    'USER_ID_CLAIM': 'user_id',
}

# ✅ Base de données PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'matchpoint',
        'USER': 'anas',
        'PASSWORD': 'Anas1234!',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

# ✅ Internationalisation
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Fichiers statiques et médias
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ Clé par défaut pour les modèles
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

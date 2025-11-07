from pathlib import Path
import os

# ============================================================
# CONFIGURACIÓN BASE DJANGO - IMPUESTO 411
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Clave de desarrollo (no usar en producción)
SECRET_KEY = 'dev-secret-key-no-usar-en-produccion'

# ⚙️ Modo depuración y hosts permitidos
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ============================================================
# APLICACIONES INSTALADAS
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tu aplicación principal
    'Impuesto_411',
]

# ============================================================
# MIDDLEWARE
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================================
# CONFIGURACIÓN DE URLS Y WSGI
# ============================================================
ROOT_URLCONF = 'Proyecto_IAW.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # carpeta global de plantillas
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

WSGI_APPLICATION = 'Proyecto_IAW.wsgi.application'

# ============================================================
# BASE DE DATOS (PostgreSQL en Docker o SQLite local)
# ============================================================
postgres_host = os.getenv('POSTGRES_HOST')

if postgres_host:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'proyecto'),
            'USER': os.getenv('POSTGRES_USER', 'proyecto'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'proyecto'),
            'HOST': postgres_host,
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ============================================================
# VALIDADORES Y AUTENTICACIÓN
# ============================================================
AUTH_PASSWORD_VALIDATORS = []

# ============================================================
# INTERNACIONALIZACIÓN
# ============================================================
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True

# ============================================================
# ARCHIVOS ESTÁTICOS
# ============================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

# ============================================================
# CONFIGURACIÓN POR DEFECTO DE CAMPOS
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

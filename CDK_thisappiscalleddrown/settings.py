"""
Paramètres de configuration de Django pour le projet CDK_thisappiscalleddrown.


DOC :
https://docs.djangoproject.com/en/3.1/topics/settings/

Paramètres et valeurs :
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import environ

root = environ.Path(__file__) - 2  # root of project
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(root() + "/.env")  # reading .env file

# Build paths inside the project like this: BASE_DIR / ...
BASE_DIR = root()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")
SITE_ID = env.int("SITE_ID")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = root()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.admindocs",
    "django.contrib.redirects",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Applications Packages / Modification de defaults
    "impostor",
    "accounts",  # Pour changer le model User
    "bootstrap4",
    "easy_maps",
    # Apps
    "CDK_thisappiscalleddrown",
    "thisappiscalleddrown",
    "thisappiscalleddrownAPI",
    # Widget Tweaks
    "widget_tweaks",
    "bootstrap_datepicker_plus",
    # Django REST Framework
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "CDK_thisappiscalleddrown.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            (BASE_DIR + "/CDK_thisappiscalleddrown/templates"),
            (BASE_DIR + "/thisappiscalleddrown/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "CDK_thisappiscalleddrown.context_processors.get_current_year_to_context",
                "CDK_thisappiscalleddrown.context_processors.get_unread_notifications_number_to_context",
            ],
        },
    },
]

WSGI_APPLICATION = "CDK_thisappiscalleddrown.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": BASE_DIR + "/my.cnf",
            "init_command": "SET sql_mode='STRICT_ALL_TABLES'; SET default_storage_engine=INNODB;",
            "use_unicode": True,
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "fr-ch"

TIME_ZONE = "Europe/Zurich"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR + "/media"

STATIC_ROOT = BASE_DIR + "/static"

STATICFILES_DIRS = [
    (BASE_DIR + "/thisappiscalleddrown/static"),
]

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "impostor.backend.AuthBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

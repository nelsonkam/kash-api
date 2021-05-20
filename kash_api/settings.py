"""
Django settings for kash_api project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
import environ
import sentry_sdk
import stripe
from celery.schedules import crontab
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration
from stellar_sdk import Asset, Network

env = environ.Env(DEBUG=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(env_file=str(BASE_DIR / ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.postgres',
    "core",
    "kash",
    "django_extensions",
    "django_hosts",
    "rest_framework",
    "corsheaders",
    "phone_verify",
    "djmoney",
    'djmoney.contrib.exchange',
    "storages",
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'request_logging.middleware.LoggingMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django_hosts.middleware.HostsResponseMiddleware'
]

ROOT_URLCONF = "kash_api.urls"
ROOT_HOSTCONF = 'kash_api.hosts'
DEFAULT_HOST = 'api'

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

WSGI_APPLICATION = "kash_api.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": env.db()}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

AUTH_USER_MODEL = "core.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "core.backends.auth.SMSAuthBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '200/day',
        'deposit': "1/minute"
    },
    "PAGE_SIZE": 20
}

SMS_BACKEND = (
    "core.backends.sms.ConsoleSMSBackend"
    if DEBUG
    else "core.backends.sms.AmazonSMSBackend"
)

PHONE_VERIFICATION = {
    "BACKEND": SMS_BACKEND,
    "OPTIONS": {},
    "TOKEN_LENGTH": 6,
    "MESSAGE": _("Your verification code for {app} is: {security_code}"),
    "APP_NAME": "Kash",
    "SECURITY_CODE_EXPIRATION_TIME": 3600 * 0.5,
    "VERIFY_SECURITY_CODE_ONLY_ONCE": False,
    "TEST_PHONE_NUMBERS": ["+22921000000", "+22921000001"]
}

SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": True,
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
}

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-shop-id",
]

APP_NAME = env('APP_NAME')

DO_SPACES_KEY = env("DO_SPACES_KEY")
DO_SPACES_SECRET = env("DO_SPACES_SECRET")
DO_SPACES_BUCKET = env("DO_SPACES_BUCKET")
DO_SPACES_REGION = env("DO_SPACES_REGION")
DO_SPACES_ENDPOINT_URL = env("DO_SPACES_ENDPOINT_URL")

SLACK_TOKEN = env("SLACK_TOKEN")
TG_CHAT_ID = env('TG_CHAT_ID')
TG_BOT_TOKEN = env('TG_BOT_TOKEN')

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = "us-east-1"

MESSAGEBIRD_ACCESS_KEY = env("MESSAGEBIRD_ACCESS_KEY")

FEDAPAY_API_KEY = env("FEDAPAY_API_KEY")

KKIAPAY_PUBLIC_KEY = env('KKIAPAY_PUBLIC_KEY')
KKIAPAY_PRIVATE_KEY = env('KKIAPAY_PRIVATE_KEY')
KKIAPAY_SECRET_KEY = env('KKIAPAY_SECRET_KEY')
RAVE_SECRET_KEY = env('RAVE_SECRET_KEY')
RAVE_PUBLIC_KEY = env('RAVE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY

CLIENT_VERSION = "1.0.0"

KWEEK_COMMISSION_RATIO = 0.05

OPEN_EXCHANGE_RATES_APP_ID = env("OPEN_EXCHANGE_RATES_APP_ID")

INTERNAL_IPS = ("127.0.0.1")

if not DEBUG:
    sentry_sdk.init(
        dsn="https://4c4f295e7f2845118ca85670803681a2@o441760.ingest.sentry.io/5416328",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

QOSIC_USERNAME = env('QOSIC_USERNAME')
QOSIC_PASSWORD = env('QOSIC_PASSWORD')
QOSIC_MOOV_MONEY_CLIENT_ID = env('QOSIC_MOOV_MONEY_CLIENT_ID')
QOSIC_MTN_MOBILE_MONEY_CLIENT_ID = env('QOSIC_MTN_MOBILE_MONEY_CLIENT_ID')
QOSIC_URL = env('QOSIC_URL')

EXCHANGE_BACKEND = 'djmoney.contrib.exchange.backends.OpenExchangeRatesBackend'

ONESIGNAL_APP_ID = env('ONESIGNAL_APP_ID')
ONESIGNAL_REST_API_KEY = env('ONESIGNAL_REST_API_KEY')

BINANCE_API_KEY = env('BINANCE_API_KEY')
BINANCE_SECRET_KEY = env('BINANCE_SECRET_KEY')
BINANCE_API_URL = env('BINANCE_API_URL')

USDC_ASSET = Asset(issuer=env("STELLAR_USDC_ISSUER"), code=env("STELLAR_USDC_CODE"))
STELLAR_MASTER_WALLET_SK = env("STELLAR_MASTER_WALLET_SK")
STELLAR_HORIZON_URL = env("STELLAR_HORIZON_URL")
STELLAR_NETWORK_PASSPHRASE = Network.PUBLIC_NETWORK_PASSPHRASE if not DEBUG else Network.TESTNET_NETWORK_PASSPHRASE

CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')

CELERY_BEAT_SCHEDULE = {
    "update_rates": {
        "task": "core.tasks.update_rates",
        "schedule": crontab(hour='*/3', minute='0'),
    },
    "check_txn_status": {
        "task": "kash.tasks.check_txn_status",
        "schedule": 15.0
    },
    "send_pending_notifications": {
        "task": "kash.tasks.send_pending_notifications",
        "schedule": crontab(minute='*/3'),
    },
} if APP_NAME == "api-server" else {}

CONVERSION_RATES = {
    'NGN_XOF': 1.20,
    'MARGIN': .1
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',  # change debug level as appropiate
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

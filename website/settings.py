"""
Django settings for website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import django.conf.global_settings as DEFAULT_SETTINGS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 'm1b^v7%4rt($x1o-_+qkw8d0zd!^&4-^r!hhwwso%jemq+ut!2')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = bool(os.environ.get('DJANGO_DEBUG', '')) or \
    'travis' in os.environ or 'scdtest' in os.environ

TEMPLATE_DEBUG = DEBUG

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'compressor',
    'ganalytics',

    'storages',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'periodically',

    'django_gravatar',
    'foundationform',

    'website',
    'external',
    'events',
    'sponsorship',
    'members',



    'django_cleanup',

)

SOCIALACCOUNT_PROVIDERS = {
    "persona": {
        "AUDIENCE": os.environ.get('PERSONA_AUDIENCE', 'http://localhost:8000')
    },
    "stackexchange": {
        "SITE": "stackoverflow"
    },
}

if 'scdtest' not in os.environ and 'travis' not in os.environ:
    INSTALLED_APPS += ('allauth.socialaccount.providers.facebook',
                       'allauth.socialaccount.providers.github',
                       'allauth.socialaccount.providers.persona',
                       'allauth.socialaccount.providers.linkedin',
                       'allauth.socialaccount.providers.stackexchange',
                       'allauth.socialaccount.providers.twitter',
                       'allauth.socialaccount.providers.google',)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default="sqlite:///db.sqlite3")
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'bower_components'),
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
    ('text/coffeescript', 'coffee --compile --stdio'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'compiled_static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    # Required by allauth template tags
    "django.core.context_processors.request",

    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",


    "events.context_processors.previous_events",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1


LOGIN_REDIRECT_URL = '/'

TEST_RUNNER = 'website.runner.CustomTestSuiteRunner'

ACCOUNT_ADAPTER = 'members.allauth_config.AccountAdapter'
ACCOUNT_EMAIL_REQUIRED = True

TEMPLATED_EMAIL_TEMPLATE_DIR = "emails/"
DEFAULT_FROM_EMAIL = 'Southampton Code Dojo <admin@southamptoncodedojo.com>'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Using SENDGRID
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True


# Notification configuration
FIRST_NOTIFICATION_TIME = 7 * 24 * 60  # 1 Week
SECOND_NOTIFICATION_TIME = 24 * 60     # 1 Day


# AWS
if not DEBUG:
    AWS_QUERYSTRING_AUTH = False
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
    MEDIA_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"


GANALYTICS_TRACKING_CODE = 'UA-13066747-5'

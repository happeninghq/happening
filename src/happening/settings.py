"""
Django settings for happening project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import dj_database_url
import importlib

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 'm1b^v7%4rt($x1o-_+qkw8d0zd!^&4-^r!hhwwso%jemq+ut!2')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = bool(os.environ.get('DJANGO_DEBUG', 'False') == 'True') or \
    'HAPPENING_TESTING' in os.environ
USE_DEBUG_TOOLBAR = DEBUG and (bool(os.environ.get('USE_DEBUG_TOOLBAR',
                                    'False') == 'True'))
USE_LIVE_DATA = bool(os.environ.get('USE_LIVE_DATA', str(not DEBUG)) == 'True')

ALLOWED_HOSTS = ['*']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Default
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # End default
                'django.template.context_processors.request',
                'admin.context_processors.admin_urls',
                'staff.context_processors.staff_urls',
                'events.context_processors.events',
                'pages.context_processors.pages',
                'happening.context_processors.site',
            ]
        }
    }
]


# Application definition

# Load all plugins
PLUGINS = []
for f in os.listdir('plugins'):
    if os.path.isdir('plugins/%s' % f) and not f == '__pycache__':
        PLUGINS.append('plugins.%s' % f)
        importlib.import_module('plugins.%s' % f)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'dry_rest_permissions',

    'widget_tweaks',
    'markdown_deux',

    'ganalytics',

    'storages',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'django_gravatar',

    'happening',
    'emails',
    'events',
    'members',
    'notifications',
    'pages',
    'staff',
    'admin',
    'payments',

    'django_cleanup',
] + PLUGINS

SOCIALACCOUNT_PROVIDERS = {
    'stackexchange': {
        'SITE': 'stackoverflow'
    },
    'github': {
        'SCOPE': ['user:email']
    }
}

if USE_DEBUG_TOOLBAR:
    INSTALLED_APPS += ['template_profiler_panel']
    INSTALLED_APPS += ['debug_toolbar']

if 'HAPPENING_TESTING' not in os.environ:
    # Only if we're not running tests should we enable social auth providers
    INSTALLED_APPS += ['allauth.socialaccount.providers.facebook',
                       'allauth.socialaccount.providers.github',
                       'allauth.socialaccount.providers.linkedin',
                       'allauth.socialaccount.providers.stackexchange',
                       'allauth.socialaccount.providers.twitter',
                       'allauth.socialaccount.providers.google']


MIDDLEWARE_CLASSES = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'happening.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'happening.middleware.VaryByHostMiddleware',
    'django.middleware.common.CommonMiddleware',
    'happening.plugins.ResolvePluginMiddlewareMiddleware',
    'members.middleware.TrackingLinkMiddleware',
]


ROOT_URLCONF = 'happening.urls'

WSGI_APPLICATION = 'happening.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
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

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'compiled_static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
]

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures'),
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'

TEST_RUNNER = 'happening.runner.CustomTestSuiteRunner'

ACCOUNT_ADAPTER = 'members.allauth_config.AccountAdapter'
ACCOUNT_EMAIL_REQUIRED = True

if not USE_LIVE_DATA:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Using SENDGRID
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', '')
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', '')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

# AWS
if USE_LIVE_DATA:
    AWS_QUERYSTRING_AUTH = False
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
    MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"


# Sentry error tracking
if USE_LIVE_DATA:
    # Set your DSN value
    RAVEN_CONFIG = {
        'dsn': os.environ['SENTRY_DSN'],
    }

    # Add raven to the list of installed apps
    INSTALLED_APPS = INSTALLED_APPS + [
        # ...
        'raven.contrib.django.raven_compat',
    ]

# For SSL redirect on Heroku
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Configure Django Debug Toolbar
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'template_profiler_panel.panels.template.TemplateProfilerPanel'
]

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': ''
}

MARKDOWN_DEUX_STYLES = {
    'default': {
        'extras': {
            'tables': None,
        },
        'safe_mode': 'escape',
    },
}


if 'HAPPENING_TESTING' in os.environ:
    # Special settings in here to speed up tests
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    DEBUG = False
    import logging
    logging.disable(logging.CRITICAL)


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'PAGE_SIZE': 10,
}


# CELERY
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/London'

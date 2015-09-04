"""
Django settings for happening project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import dj_database_url
import django.conf.global_settings as DEFAULT_SETTINGS
import importlib

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

# Don't force SSL locally
SSLIFY_DISABLE = DEBUG

ALLOWED_HOSTS = ["*"]


# Application definition

# Load all plugins
PLUGINS = []
for f in os.listdir("plugins"):
    if os.path.isdir("plugins/%s" % f):
        PLUGINS.append("plugins.%s" % f)
        importlib.import_module("plugins.%s" % f)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'widget_tweaks',
    'markdown_deux',

    'compressor',
    'sekizai',
    'ganalytics',

    'storages',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'periodically',

    'django_gravatar',

    'debug_toolbar',
    'template_profiler_panel',

    'happening',
    'emails',
    'external',
    'events',
    'members',
    'notifications',
    'pages',
    'voting',
    'staff',
    'admin',
    'payments',

    'django_cleanup',
) + tuple(PLUGINS)

SOCIALACCOUNT_PROVIDERS = {
    "persona": {
        "AUDIENCE": os.environ.get('PERSONA_AUDIENCE', 'http://localhost:8000')
    },
    "stackexchange": {
        "SITE": "stackoverflow"
    },
}

if 'scdtest' not in os.environ and 'travis' not in os.environ:
    # Only if we're not running tests should we enable social auth providers
    INSTALLED_APPS += ('allauth.socialaccount.providers.facebook',
                       'allauth.socialaccount.providers.github',
                       'allauth.socialaccount.providers.persona',
                       'allauth.socialaccount.providers.linkedin',
                       'allauth.socialaccount.providers.stackexchange',
                       'allauth.socialaccount.providers.twitter',
                       'allauth.socialaccount.providers.google',)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'happening.middleware.VaryByHostMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
)


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

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'bower_components'),
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
    ('text/ecmascript-6', 'babel {infile}'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'compiled_static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = not DEBUG

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",

    "sekizai.context_processors.sekizai",

    "admin.context_processors.admin_urls",
    "staff.context_processors.staff_urls",
    "events.context_processors.events",
    "pages.context_processors.pages",
    "happening.context_processors.site",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    # "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'

TEST_RUNNER = 'happening.runner.CustomTestSuiteRunner'

ACCOUNT_ADAPTER = 'members.allauth_config.AccountAdapter'
ACCOUNT_EMAIL_REQUIRED = True

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Using SENDGRID
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

# AWS
if not DEBUG:
    AWS_QUERYSTRING_AUTH = False
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
    MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"


# Sentry error tracking
if not DEBUG:
    # Set your DSN value
    RAVEN_CONFIG = {
        'dsn': 'https://ebd16d59c09c45dc87ebdf7d27e8bd08:' +
               '64f24482964b43d7847f2af6828e96b7@app.getsentry.com/36991',
    }

    # Add raven to the list of installed apps
    INSTALLED_APPS = INSTALLED_APPS + (
        # ...
        'raven.contrib.django.raven_compat',
    )

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
    # 'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'template_profiler_panel.panels.template.TemplateProfilerPanel'
]

DEBUG_TOOLBAR_CONFIG = {
    "JQUERY_URL": ""
}

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "tables": None,
        },
        "safe_mode": "escape",
    },
}

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': os.environ.get('MEMCACHEDCLOUD_SERVERS'),
            'USERNAME': os.environ.get('MEMCACHEDCLOUD_USERNAME'),
            'PASSWORD': os.environ.get('MEMCACHEDCLOUD_PASSWORD')
        }
    }

CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = ""

plugin_files = ['blocks',
                'actions',
                'notifications']

for app in INSTALLED_APPS:
    f = app.replace(".", "/")
    for p in plugin_files:
        if os.path.isfile("%s/%s.py" % (f, p)):
            importlib.import_module("%s.%s" % (app, p))


if 'scdtest' in os.environ:
    # Special settings in here to speed up tests
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    COMPRESS_ENABLED = False
    COMPRESS_OFFLINE = False
    DEBUG = False
    TEMPLATE_DEBUG = False
    import logging
    logging.disable(logging.CRITICAL)

    # TODO: Write replacement templatetags that do nothing.
    COMPRESS_PRECOMPILERS = (
        ('text/x-scss', 'echo'),
        ('text/ecmascript-6', 'echo'),
    )

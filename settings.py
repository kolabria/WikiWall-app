# Django settings for kolabria - sqlproject.
from mongoengine import connect
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DIRNAME = os.path.dirname(__file__)

PROJECT_PATH = os.path.realpath(DIRNAME)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

ADMIN_MEDIA_PREFIX = '/static/admin/'

MANAGERS = ADMINS

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

# Database settings
connect('kolabria-mongo')

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True,
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar_mongo.panel.MongoDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
#    'debug_toolbar.panels.logger.LoggingPanel',
)

# Email Configuration for password recovery, etc.
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = "587"
EMAIL_HOST_USER = 'kolabria.test@gmail.com'
EMAIL_HOST_PASSWORD = 'kolabria1234test'
EMAIL_USE_TLS = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'debug_toolbar_mongo',
)

INTERNAL_IPS = ('127.0.0.1',)
LANGUAGE_CODE = 'en-us'
LOGIN_REDIRECT_URL = '/private'
LOGIN_URL = '/login'

MEDIA_URL = '/media/'
MEDIA_PATH = os.path.join(PROJECT_PATH, 'media')
MEDIA_ROOT = '/home/alok/kolabria/kolabria/media'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'kolabria.urls'
SECRET_KEY = '&lx4lr@=vkjls72!45+wp0dkvi*r-q_npgll4_-novi0s%lv+x'
SESSION_ENGINE = 'mongoengine.django.sessions'
SITE_ID = 1

STATIC_URL = '/static/'
STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
STATICFILES_DIRS = (
    STATIC_PATH,
)

TEMPLAGE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
    'context_processors.auth',
    'context_processors.site_info',
)

TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, "templates"))
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)
TIME_ZONE = 'America/Montreal'
USE_I18N = False

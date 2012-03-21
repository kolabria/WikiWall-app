# Django settings for crop project.
import os
import django
import logging
from mongoengine import connect

DIRNAME = os.path.dirname(__file__)
PROJECT_PATH = os.path.realpath(DIRNAME)
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = getattr(settings_local, 'DEBUG', True)
TEMPLATE_DEBUG = DEBUG

CONTACT_DEBUG = False
DJANGO_SERVER = getattr(settings_local, 'DJANGO_SERVER', False)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = "587"
EMAIL_HOST_USER = 'kolabria.test@gmail.com'
EMAIL_HOST_PASSWORD = 'kolabria1234test'
DEFAULT_FROM_EMAIL = 'noreply@kolabria.com'
EMAIL_USE_TLS = True

ADMINS = (
     ('ted', 'ted@kolabria.com'),
     ('alok', 'alok.mohindra@gmail.com'),
  # ('Your Name', 'your_email@domain.com'),
)

ADMIN_MEDIA_PREFIX = '/static/admin/'
MANAGERS = ADMINS

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
#    'django.contrib.messages',
    'django.contrib.sessions',
#    'django.contrib.sites',
    'django.contrib.staticfiles',
#    'bootstrap',
    'crispy_forms',
    'mongoforms',
    'debug_toolbar',
    'debug_toolbar_mongo',
)

INTERNAL_IPS = ('127.0.0.1',)
LANGUAGE_CODE = 'en-us'
USE_I18N = False
LOGIN_REDIRECT_URL = '/walls'
LOGIN_URL = '/login'

MEDIA_URL = '/media/'
MEDIA_PATH = os.path.join(PROJECT_PATH, 'media')
MEDIA_ROOT = '/home/alok/kolabria/kolabria/media'
#MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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
#    'django.contrib.messages.middleware.MessageMiddleware',
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

# import settings_local if it exists to override specific settings otherwise
# user settings_local_default
try:
    import settings_local
except:
    import settings_dev as settings_local

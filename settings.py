# Django settings for kolabria - sqlproject.

import os

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

ADMIN_MEDIA_PREFIX = '/static/admin/'

MANAGERS = ADMINS





# Database settings


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'mysql' or 'sqlite3'
        'NAME': 'data/data.db',  # Or path to database file if using sqlite3.
        'USER': '',     # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '',     # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',     # Set to empty string for default. Not used with sqlite3.
    }
}


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True,
}





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
    'kolabria.home',
    'kolabria.walls',
    'south',
)


INTERNAL_IPS = ('127.0.0.1',)
LANGUAGE_CODE = 'en-us'
LOGIN_REDIRECT_URL = '/private'
LOGIN_URL = '/login'
MEDIA_ROOT = '/home/alok/kolabria/kolabria/media'
MEDIA_URL = '/media/'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
#    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'kolabria.urls'
SECRET_KEY = '&lx4lr@=vkjls72!45+wp0dkvi*r-q_npgll4_-novi0s%lv+x'

SITE_ID = 1
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    "/home/alok/kolabria/kolabria/static/",
)

TEMPLATE_CONTEXT_PROCESSORS = (
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

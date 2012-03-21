import os.path
from mongoengine import connect
from settings import PROJECT_ROOT

# Mongo Database settings
#TODO setup mongo to read from correct database
connect('kolabria-new')

DEBUG = False
DJANGO_SERVER = True

# Mongo Database settings
#TODO setup mongo to read from correct database
connect('kolabria-new')

INSTALLED_APPS += (
    'debug_toolbar',
    'debug_toolbar_mongo',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
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

INSTALLED_APPS += (
#    'another_app',
)

MEDIA_PATH = os.path.join(PROJECT_PATH, 'media')
MEDIA_ROOT = '/srv/www/public_html/static/'
#MEDIA_ROOT = '/home/alok/kolabria/kolabria/media'

STATICFILES_DIRS += (
    '/srv/www/public_html/static/',
)

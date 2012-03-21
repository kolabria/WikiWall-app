import os.path
from mongoengine import connect
from settings import PROJECT_ROOT

DEBUG = TEMPLATE_DEBUG = False
DJANGO_SERVER = True

# Mongo Database settings
#TODO setup mongo to read from correct database
connect('kolabria-new')

INSTALLED_APPS += (
#    'prod_only_module',
)

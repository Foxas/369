from web369.conf.base import *
from pkg_resources import resource_filename

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = (
    '127.0.0.1',
)

CACHE_BACKEND = "dummy://"

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'web369',
)

ROOT_URLCONF = 'web369.urls.designer'

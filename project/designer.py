from project.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BUILDOUT_DIR, 'var', 'mail')

CACHE_BACKEND = "dummy://"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BUILDOUT_DIR, 'var', 'development.db'),
    }
}

ROOT_URLCONF = 'project.designer_urls'

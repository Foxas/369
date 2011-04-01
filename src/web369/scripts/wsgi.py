import os
import django.core.handlers.wsgi


def get_application():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web369.settings'
    return django.core.handlers.wsgi.WSGIHandler()


application = get_application()


def load(globals_):
    """ This method is used in buildout to generate wsgi script """
    globals_['application'] = application

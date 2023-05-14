"""Development Environment
"""
import os

LOG_DIR = os.path.join(".log")

DEBUG = True


INSTALLED_APPS = [
    'daphne',
    'ams.apps.ASMAdminConfig',#'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', 'request', 'django_extensions'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'ERROR': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'filename': os.path.join(LOG_DIR, 'errors.log')
        },
        'CRITICAL': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'filename': os.path.join(LOG_DIR, 'critical.log')
        },
        'WARNING': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'filename': os.path.join(LOG_DIR, 'warnings.log')
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['ERROR', 'WARNING', 'CRITICAL', 'console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}


#django-debug-toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

#django-request
REQUEST_BASE_URL = "http://127.0.0.1"
REQUEST_IGNORE_PATHS = (
    r'^__debug__/',
    r'^static/',
)

# Production Environment

import os

from .settings_base import BASE_DIR


LOG_DIR = os.path.join("/", "log")


DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, '.static')

INSTALLED_APPS = [
    'daphne',
    'asm.apps.ASMAdminConfig', #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', 'request', 'django_extensions'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'HOST': 'db_host',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_persian_ci',
        'TEST': {
            'NAME': 'test_database',
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_persian_ci',
        }
    },
}

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

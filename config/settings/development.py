"""
Django development settings for Worklane project.
"""

from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = ['*']

# Database — SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email — console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files — no whitenoise compression in dev
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

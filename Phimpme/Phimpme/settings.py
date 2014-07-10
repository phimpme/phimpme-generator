"""
Django settings for Phimpme project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4&w*_6stda4l1gx71o26^zw0))loa!d*+a!96h_amd9&bd4myj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
    'Phimpme.apps.usermgt',
    'Phimpme.apps.orders',
    'Phimpme.apps.appshop',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Phimpme.urls'

WSGI_APPLICATION = 'Phimpme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = False

# Default content type and charset to use for all HttpResponse objects, if a
# MIME type isn't manually specified. These are used to construct the
# Content-Type header.
DEFAULT_CONTENT_TYPE = 'text/html'
DEFAULT_CHARSET = 'utf-8'

# Encoding of files read from disk (template and initial SQL files).
FILE_CHARSET = 'utf-8'
# Email address that error messages come from.
SERVER_EMAIL = 'root@localhost'

############
# SESSIONS #
############
SESSION_COOKIE_NAME = 'sessionid'  # Cookie name. This can be whatever you want.
SESSION_COOKIE_AGE = 60 * 30  # Age of cookie, in seconds (default: 2 weeks).
SESSION_SAVE_EVERY_REQUEST = True
SESSION_CLEAR_INTERVAL = 60  # sesseion timeout, in seconds


# media path
MEDIA_ROOT = BASE_DIR + '/media/'
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_DIR1 = BASE_DIR + '/Phimpme/static/'
STATICFILES_DIRS = (
    STATIC_DIR1,
)
STATIC_URL = '/static/'

LOGIN_URL = '/static/login.html'
LOGOUT_URL = '/static/login.html'
LOGIN_REDIRECT_URL = LOGIN_URL

# APP OUT PUT PATH
OUTPUT_PATH = STATIC_DIR1 + 'generated_apk' + '%Y/%m/%d/'



# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


TEMPLATE_DIR = BASE_DIR + '/Phimpme/static'
# TEMPLATE_DIRS
TEMPLATE_DIRS = (
    TEMPLATE_DIR,
)

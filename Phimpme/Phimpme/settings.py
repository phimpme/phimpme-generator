"""
Django settingsfor Phimpme project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import EMAIL_PORT, EMAIL_HOST_USER, \
    EMAIL_HOST_PASSWORD, EMAIL_USE_TLS
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4&w*_6stda4l1gx71o26^zw0))loa!d*+a!96h_amd9&bd4myj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

DOMAIN_NAME = '192.168.56.101:8000'
# Paypal options
PAYPAL_MODE = 'sandbox'  # sandbox or live
PAYPAL_CLIENT_ID = 'AUVEihBfbBCQzLxaTjNdhzV16yI-PvQEHDJblP6P4Ba1Fr5cu_CAZdO0-5IM'
PAYPAL_CLIENT_SECRET = 'EF5uIBClqoo--0oIhKeFtaa-ciCgL34WDkhyQbBslM7_MHZe2DHkNJTAM9pD'

# Application definition
import sys

sys.path.insert(0, os.path.join(BASE_DIR, 'site-packages'))

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
	'paypalrestsdk',
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
	# 'default': {
	# 'ENGINE': 'django.db.backends.mysql',
	#     'NAME': 'Phimpme',
	#     'HOST': 'localhost',
	#     'USER': 'root',
	#     'PASSWORD': 'root',
	#     'OPTIONS':{
	#         'init_command':'SET storage_engine=INNODB',
	#     },
	# }
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
OUTPUT_PATH = STATIC_DIR1 + 'output_path'



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



# configure email host
EMAIL_HOST = 'smtp.qq.com'  # SMTP server
EMAIL_PORT = 25  # SMTP port
EMAIL_HOST_USER = 'xxxxxxx@qq.com'  # E-mail address
EMAIL_HOST_PASSWORD = 'xxxxxxxx'
# EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

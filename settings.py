# Django settings for USEmbassy_backend project.
# -*- coding: utf-8 -*-

import os
from settings_local import *

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

#String conf
DEVICE_TOKEN_LENGTH = 80
REGISTRATION_IDS_LENGTH = 200

BANNER_TITLE_LENGTH = 40
BANNER_DESCRIPTION_LENGTH = 60

# enforced on form level
BANNER_TITLE_LEN = 20
BANNER_TEXT_LEN = 50

FILE_TITLE_LENGTH = 120

TITLE_LENGTH = 80
DESCRIPTION_LENGTH = 1024
TEXT_LENGTH = 5000
LONG_TEXT_LENGTH = 20000
URL_LENGTH = 512

BITRATE1 = 1000
BITRATE2 = 500
BITRATE3 = 56

LOGIN_REDIRECT_URL = '/'

TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Artur Bacmaga', 'artur.bacmaga@agitive.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
VIDEO_ROOT = os.path.join(MEDIA_ROOT, 'video')
FILE_UPLOAD_TEMP_DIR = os.path.join(PROJECT_PATH, 'tmp')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static_collected')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
	#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'core.middleware.PasswordChangeMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_PROFILE_MODULE = 'core.UserProfile'

ROOT_URLCONF = 'USEmbassy_backend.urls'

# celery, check this backend if compatible with new celery
#IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = 'imagekit.cachefiles.backends.Async'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'USEmbassy_backend.wsgi.application'

TEMPLATE_DIRS = (
	os.path.join(PROJECT_PATH, '', 'templates'),
)

FIXTURE_DIRS = (
	os.path.join(PROJECT_PATH, '', 'fixtures'),
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django_extensions',
	'djcelery_email',
	'push_notifications',
	'imagekit',
	'south',
	'raven.contrib.django.raven_compat',
	'push_notification',
	'page',
	'video',
	'banner',
	'file_manager',
	'feedback',
	'images',
	'core',
	'rss',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

# celery config
from datetime import timedelta

CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_RESULT_SERIALIZER = 'pickle'

CELERYBEAT_SCHEDULE = {
	'ios-device-feedback': {
		'task': 'push_notification.tasks.get_ios_device_feedback',
		'schedule': timedelta(days=1),
		'relative': True,
	}
}

if IS_MASTER:
	CELERYBEAT_SCHEDULE.update({
		'get-news-every-hour': {
			'task': 'rss.tasks.get_all_news',
			'schedule': timedelta(hours=1),
			'relative': True,
		},

		'media-daily-sync': {
			'task': 'core.tasks.sync_media',
			'schedule': timedelta(days=1),
			'relative': True,
		}
	})

"""
Django settings for your TOM project.

Originally generated by 'django-admin startproject' using Django 2.1.1.
Generated by ./manage.py tom_setup on Jan. 13, 2020, 10:58 p.m.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import ast
import tempfile





# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY','+xg%_n7l==$@v7))t1&amp;@a_tl)qo$=g7rl^wp7bx^qu+g7+hiaj')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ast.literal_eval(os.getenv('DJANGO_DEBUG', 'False'))

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'guardian',
    'tom_common',
    'django_comments',
    'bootstrap4',
    'crispy_forms',
    'django_filters',
    'django_gravatar',
    'rest_framework',
    'tom_targets',
    'tom_alerts',
    'tom_catalogs',
    'tom_observations',
    'tom_dataproducts',
    'mop',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tom_common.middleware.ExternalServiceMiddleware',
]

ROOT_URLCONF = 'mop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'mop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
       'NAME': os.getenv('DB_NAME', 'mop'),
       'USER': os.getenv('DB_USER', 'postgres'),
       'PASSWORD': os.getenv('DB_PASS', ''),
       'HOST': os.getenv('DB_HOST', '127.0.0.1'),
       'PORT': os.getenv('DB_PORT', '5432'),
   },

    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },




}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:m:s'
DATE_FORMAT = 'Y-m-d'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'data')
MEDIA_URL = '/data/'

#Using AWS

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_S3_BUCKET', '')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-west-2')
AWS_DEFAULT_ACL = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
}

# Caching
# https://docs.djangoproject.com/en/dev/topics/cache/#filesystem-caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': tempfile.gettempdir()
    }
}



# TOM Specific configuration
TARGET_TYPE = 'SIDEREAL'

FACILITIES = {
    'LCO': {
        'portal_url': 'https://observe.lco.global',
        'api_key': os.environ.get('LCO_API_KEY','dummy'),
    },
    'GEM': {
        'portal_url': {
            'GS': 'https://139.229.34.15:8443',
            'GN': 'https://128.171.88.221:8443',
        },
        'api_key': {
            'GS': os.environ.get('GEMINI_S_API_KEY','dummy'),
            'GN': os.environ.get('GEMINI_N_API_KEY','dummy'),
        },
        'user_email':  os.environ.get('GEMINI_USERNAME','dummy'),
        'programs': {
            'GS-2020A-DD-104': {
                '8':  'GMOS Aquisiton 0.75arcsec',
                '9':  'Std: R400 LongSlit 0.75arcsec for Blue Objects',
                '12': 'Std: B600 LongSlit 0.75arcsec for Red Objects',
            },
            'GN-2020A-DD-104': {
                  '8': 'GMOS Aquisiton 0.75arcsec',
                  '9': 'Std: R400 LongSlit 0.75arcsec for Red Objects',
                  '17': 'Std: B600 LongSlit 0.75arcsec for Blue Objects',
           },
        },
    },
}



# Define the valid data product types for your TOM. Be careful when removing items, as previously valid types will no
# longer be valid, and may cause issues unless the offending records are modified.
DATA_TYPES = (
    ('SPECTROSCOPY', 'Spectroscopy'),
    ('PHOTOMETRY', 'Photometry')
)

DATA_PRODUCT_TYPES = {
    'photometry': ('photometry', 'Photometry'),
    'fits_file': ('fits_file', 'FITS File'),
    'spectroscopy': ('spectroscopy', 'Spectroscopy'),
    'image_file': ('image_file', 'Image File'),
    'TAP_priority': ('TAP_priority', 'TAP Priority'),
    'lc_model': ('lc_model', 'Model'),
}

DATA_PROCESSORS = {

    'photometry': 'mop.processors.photometry_processor.PhotometryProcessor',
    'spectroscopy': 'mop.processors.spectroscopy_processor.SpectroscopyProcessor',
}

TOM_FACILITY_CLASSES = [
    'tom_observations.facilities.lco.LCOFacility',
    'tom_observations.facilities.gemini.GEMFacility',
    'tom_observations.facilities.soar.SOARFacility',
    'tom_observations.facilities.lt.LTFacility'
]

TOM_ALERT_CLASSES = [
    'tom_alerts.brokers.mars.MARSBroker',
    'tom_alerts.brokers.lasair.LasairBroker',
    'tom_alerts.brokers.scout.ScoutBroker',
    'tom_alerts.brokers.tns.TNSBroker',
    'tom_alerts.brokers.gaia.GaiaBroker',
    
]
#'tom_antares.antares.AntaresBroker',
#BROKER_CREDENTIALS = {}

#'antares': {
#        'api_key': os.environ.get('ANTARES_KEY','dummy'),
#        'api_secret': os.environ.get('ANTARES_PASSWORD','dummy')
#}

# Define extra target fields here. Types can be any of "number", "string", "boolean" or "datetime"
# See https://tomtoolkit.github.io/docs/target_fields for documentation on this feature
# For example:
# EXTRA_FIELDS = [
#     {'name': 'redshift', 'type': 'number'},
#     {'name': 'discoverer', 'type': 'string'}
#     {'name': 'eligible', 'type': 'boolean'},
#     {'name': 'dicovery_date', 'type': 'datetime'}
# ]
EXTRA_FIELDS = [{'name':'Alive','type':'boolean', 'default':True},
                {'name':'Classification','type':'string','default':'Microlensing PSPL'},
                {'name':'Observing_mode','type':'string','default':'No'},
                {'name':'t0','type':'number','default':0},
                {'name':'u0','type':'number','default':0},
                {'name':'tE','type':'number','default':0},
                {'name':'piEN','type':'number','default':0},
                {'name':'piEE','type':'number','default':0},
                {'name':'Source_magnitude','type':'number','default':0},
                {'name':'Blend_magnitude','type':'number','default':0},
                {'name':'Baseline_magnitude','type':'number','default':0},
                {'name':'Fit_covariance','type':'string','default':''},
                {'name':'TAP_priority','type':'number','default':''},
                {'name':'Spectras','type':'number','default':0},
                {'name':'Last_fit','type':'number','default':2446756.50000}]
       

TARGET_PERMISSIONS_ONLY=True

# Authentication strategy can either be LOCKED (required login for all views)
# or READ_ONLY (read only access to views)
AUTH_STRATEGY = 'READ_ONLY'

# URLs that should be allowed access even with AUTH_STRATEGY = LOCKED
# for example: OPEN_URLS = ['/', '/about']
OPEN_URLS = ['/mop/Home']

HOOKS = {
    'target_post_save': 'tom_common.hooks.target_post_save',
    'observation_change_state': 'tom_common.hooks.observation_change_state',
    'data_product_post_upload': 'tom_dataproducts.hooks.data_product_post_upload'
}

AUTO_THUMBNAILS = False

THUMBNAIL_MAX_SIZE = (0, 0)

THUMBNAIL_DEFAULT_SIZE = (200, 200)

HINTS_ENABLED = True
HINT_LEVEL = 20

try:
    from local_settings import * # noqa
except ImportError:
    pass

"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from django.utils.translation import ugettext_lazy as _
import os
import psycopg2
import django.contrib.auth
django.contrib.auth.LOGIN_URL = '/'



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xnw^-qf5hc_&^evh$*3igr9i#i31v5h-hfwn#014n8s011)x*g'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['classscanner.herokuapp', '127.0.0.1', '0.0.0.0']
ALLOWED_HOSTS = ['*']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #my apps
    'scanner',
    #3rd party apps
    'django_celery_results',
    'django_celery_beat',
    'phonenumber_field',
]

PHONENUMBER_DB_FORMAT = 'E164'

# AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',) 
AUTHENTICATION_BACKENDS = ['mysite.mybackend.MyBackend']


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'shivaum7@gmail.com'
EMAIL_HOST_PASSWORD = 'Shivaum5j'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'ClassScanner <noreply@noreply.com>'



# DEVELOPEMENT

# BROKER_URL = 'amqp://guest:guest@localhost:5672/'
# CELERY_RESULT_BACKEND = 'django-db'
# # CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# # CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'


# PRODUCTION

CLOUDAMQP_URL = "amqp://skleicus:43L_q0Y8ReOHuB120dBXohFf7KaH2TOQ@salamander.rmq.cloudamqp.com/skleicus"
# REDIS_URL = "redis://h:p74f792c08d3e92e1048b157221d6e892ac36278f131fcd506f2c7bdcfc8e40e5@ec2-34-206-56-140.compute-1.amazonaws.com:16419"
BROKER_URL = CLOUDAMQP_URL
BROKER_POOL_LIMIT = 0
BROKER_CONNECTION_MAX_RETRIES = None

CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json", "msgpack"]
# CELERY_RESULT_BACKEND = 'None'
CELERY_RESULT_BACKEND = 'rpc'
CELERY_IMPORTS = ['scanner.tasks']

BROKER_HEARTBEAT = None 
BROKER_CONNECTION_TIMEOUT = 30
CELERY_SEND_EVENTS = False
CELERY_EVENT_QUEUE_EXPIRES = 60




MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #custom middleware   
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [   os.path.join(BASE_DIR, 'templates'),

                ],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


# DEVLOPMENT

# DATABASES = {
# 'default': {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'ClassScanner',
#     'HOST': '127.0.0.1',
#     'PORT': '3306',
#     'USER': 'root',
#     'PASSWORD': '',
# }}


# PRODUCTION

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',     #JAWSDB
    #     'NAME': 'dt5vwm7s94n0m29v',
    #     'HOST': 'y0nkiij6humroewt.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
    #     'PORT': '3306',
    #     'USER': 'bqjd0v8wfmiuncm4',
    #     'PASSWORD': 'a78auhhdfmutavcm',
    #     'OPTIONS': {
    #         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    #     },
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dfj6hk56p0c4eu',
        'HOST': 'ec2-54-227-237-223.compute-1.amazonaws.com',
        'PORT': '5432',
        'USER': 'mcdybyosflwgqj',
        'PASSWORD': '63b3120f99491ad81bf08d6f2f41c2d1a16e575f090d804df1de1fbf01d63bc1',
    }
}






# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'scanner.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'America/Los_Angeles'
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    ('css', os.path.join(STATIC_ROOT, 'css')),
    ('js', os.path.join(STATIC_ROOT, 'js')),
    ('images', os.path.join(STATIC_ROOT, 'images')),

)



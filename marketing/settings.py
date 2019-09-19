"""
Django settings for marketing project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#-n976o+be0s+#@nq2w-2$(g&&2qclen7=&=srr4udf2wtx@jc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jet',
    'jet.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Handling all User Account
    'accounts.apps.AccountsConfig',
    
    #Adds on
    'crispy_forms',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'rest_framework',
    'django_filters',
    'bootstrap_modal_forms',
    #handling our crm content
    'crm_blog.apps.CrmBlogConfig',
    #handling  adding cm  set details
    'centermanager',
    'multiselectfield',
    'marketinghead',
    'centerbusinessmanager',
    'registrar',
    'careerconsultant',
    'partial_date',
    #phone
    'phonenumber_field',
    
]

#Registering our own Custom User
AUTH_USER_MODEL = 'accounts.UserMarketingProfile'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'marketing.urls'

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

WSGI_APPLICATION = 'marketing.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'capstone',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'AUTOCOMMIT':True,
        'ATOMIC_REQUEST': False,
        'charset': 'utf8mb4',
        
        'init_command': 'SET innodb_strict_mode=1',
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"',
            'init_command': 'SET sql_mode="STRICT_ALL_TABLES"',
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci',
        }
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Setting Phone Number
PHONENUMBER_DEFAULT_REGION = 'PH'
PHONENUMBER_DB_FORMAT =True
INTERNATIONAL = True
NATIONAL = True
RFC3966 = True

LOGIN_REDIRECT_URL = 'crm_blog:home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static' )
STATIC_URL = '/static/'
STATICFILES_DIRS = (
     os.path.join(BASE_DIR, 'statics'),
)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

JET_DEFAULT_THEME = 'light-gray'

MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
MEDIA_URL   = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

BOOTSTRAP4 = {
    'include_jquery': True,
}



''' DJANGO REST SETTINGS  '''



DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)


DEFAULT_PARSER_CLASSES = (
    'rest_framework.parsers.JSONParser',
    'rest_framework.parsers.FormParser',
    'rest_framework.parsers.MultiPartParser'
)


DEFAULT_AUTHENTICATION_CLASSES = (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication'
)


DEFAUKT_PERMISSION_CLASSES = (
    'rest_framework.permissions.AllowAny',
)

"""
Django settings for ConfigManageTool project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c42_kezdpi7zlck_7=)*8=s!n(zxns!lie)y@@f&*&$162yzdg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'RulesetComparer',
    'common',
    'permission',
    'zeep',
    'lxml',
    'xhtml2pdf',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ConfigManageTool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',
                 'templates/registration',
                 'templates/ruleset',
                 'templates/ruleset/frontend',
                 'templates/ruleset/frontend/component',
                 'templates/ruleset/backend',
                 'templates/ruleset/backend/component',
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
DATE_INPUT_FORMATS = ["%Y/%m/%d %H:%M:%S"]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "static"),
    # os.path.join(BASE_DIR, "resource"),
]

WSGI_APPLICATION = 'ConfigManageTool.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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

ADMINS = ("Wendy", "wendy.wu@audatex.com")
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

LOGIN_URL = '/accounts/login/'
STATIC_URL = '/static/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/ConfigManageTool/admin_console/ruleset/'
B2B_RULE_SET_CLIENT = 'http://%s/b2b/services/BRERuleSetAssignmentService_v1?wsdl'

UNICODE_ENCODING = 'utf-8'

COMPARE_RESULT_PATH = BASE_DIR + "/RulesetComparer/compare_result/%s"

GIT_REMOTE_NAME = 'origin'
GIT_BRANCH_MASTER = 'master'
GIT_BRANCH_DEVELOP = 'develop'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = 'media/'
STATIC_ROOT = 'static/'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'CHANGE_FOR_PRODUCTION'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'achilles',
    'simplecounter',
)
ROOT_URLCONF = 'simplecounter.urls'

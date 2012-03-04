# Django settings for phytosanitary project.

import os
DIRNAME = os.path.dirname(__file__)

TIME_FORMAT = 'H-i-s'
DATE_FORMAT = 'Y-F-j'# This is used by the SelectDateWidget in django.forms.extras.widgets http://stackoverflow.com/a/6137099/412329
DATETIME_FORMAT = 'Y-F-j H-i-s' 

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Simon Griffee', 'simon@hypertexthero.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

MEDIA_ROOT = os.path.join(DIRNAME, 'uploads')
STATIC_ROOT = os.path.join(DIRNAME, 'static')

# ln -s ~/django_projects/phytosanitary-env/lib/python2.6/site-packages/django/contrib/admin/media/ ~/django_projects/phytosanitary-env/phytosanitary-project/static/admin
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/static/",
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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    # need to add the following so user variables such as username are available in templates - https://docs.djangoproject.com/en/dev/ref/templates/api/#django-contrib-auth-context-processors-auth
    'django.contrib.auth.context_processors.auth', 
    'django.contrib.messages.context_processors.messages',
    # display django version in footer using template tag defined in context_processors.py - http://stackoverflow.com/questions/4256145/django-template-tag-to-display-django-version
    # 'phytosanitary.context_processors.django_version',
    # required to have login form on every page and for templatetags - http://stackoverflow.com/questions/2734055/putting-a-django-login-form-on-every-page
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates')
)

# django-userena - http://docs.django-userena.org/en/latest/settings.html#userena-settings
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
AUTH_PROFILE_MODULE = 'phytosanitary.Contributor'
ANONYMOUS_USER_ID = '-1'
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
USERENA_ACTIVATION_DAYS = 7
USERENA_MUGSHOT_PATH = 'user/photos/%Y/%m/'
USERENA_WITHOUT_USERNAMES = False
# USERENA_DISABLE_PROFILE_LIST = True

ROOT_URLCONF = 'phytosanitary-project.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites', # don't need this as using one site only
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    # enabling markup so we can have markdown. requires http://www.freewisdom.org/projects/python-markdown
    'django.contrib.markup',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'phytosanitary',
    'tagging',
    'userena',
    'guardian',
    'easy_thumbnails',
    'gunicorn',
    # 'south',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

# database, secret key, etc are in settings_local.py
try:
    from settings_local import *
except ImportError:
    pass
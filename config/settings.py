# Django settings for SpkrBar project.
import os

DEBUG = True
GEARS_DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Raymond Chandler III', 'raymondchandleriii@gmail.com')
)

MANAGERS = ADMINS

APPEND_SLASH = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spkrbar',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'spkrbar',
        'PASSWORD': 'spkrbar',
        'HOST': '127.0.0.1',
        'PORT': '',                      # Set to empty string for default.
    }
}

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'spkrbot@spkrbar.com'

EMAIL_USE_TLS       = True
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_HOST_USER     = 'spkrbot@spkrbar.com'
EMAIL_HOST_PASSWORD = 'KingBotOfAwesome'
EMAIL_PORT          = 587

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'core.SpkrbarUser'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
)

LOGIN_URL = '/login'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

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
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/Users/raymond/Projects/SpkrBar/SpkrBar/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/Users/raymond/Projects/SpkrBar/SpkrBar/static'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

STATICFILES_DIRS = ()

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '13ao#=90!5le^7k5*ifk)^1cx@@qm+#0===p#umxctday@%#r$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'hamlpy.template.loaders.HamlPyFilesystemLoader',
    'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "config.context_processors.include_user"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'config.wsgi.application'

TINYMCE_PLUGINS = """advhr,fullpage,preview,advimage,fullscreen,
advlink,iespell,advlist,inlinepopups,searchreplace,autolink,
insertdatetime,spellchecker,autoresize,layer,legacyoutput,
tabfocus,bbcode,lists,table,contextmenu,media,nonbreaking,visualblocks,
emotions,noneditable,visualchars,pagebreak,wordcount,paste,xhtmlxtras"""

TINYMCE_DEFAULT_CONFIG = {
    'plugins': TINYMCE_PLUGINS,
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

INSTALLED_APPS = (
    'gunicorn',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_markdown',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.markup',
    'django_gears',
    'south',
    'rest_framework',
    'core',
    'locations',
    'talks',
    'engagements',
    'blog',
    'mobile',
    'feedback'
)

if DEBUG:
    LOG_ROOT = '/Users/raymond/Projects/SpkrBar/SpkrBar/'
    TEMPLATE_DIRS = ('/Users/raymond/Projects/SpkrBar/SpkrBar/templates',)
else:
    LOG_ROOT = '/home/spkrbar/SpkrBar/'
    TEMPLATE_DIRS = ('/home/spkrbar/SpkrBar/templates',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + '/log',
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'db_logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + '/db_log',
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console', 'db_logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'less': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'coffeescript': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}
        
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

GEARS_ROOT = os.path.join(PROJECT_ROOT, 'static')

GEARS_DIRS = (
    os.path.join(PROJECT_ROOT, 'assets'),
)

GEARS_COMPILERS = {
    '.less': 'gears_less.LESSCompiler',
    '.coffee': 'gears_coffeescript.CoffeeScriptCompiler',
    '.hbs': 'gears_handlebars.HandlebarsCompiler'
}

GEARS_PUBLIC_ASSETS = (
    lambda path: not any(path.endswith(ext) for ext in ('.css', '.js')),
    r'^css/style\.css$',
    r'^vendor/css/style\.css$',
    r'^js/script\.js$',
    r'^vendor/js/script\.js$',
)

GEARS_FINGERPRINTING = False

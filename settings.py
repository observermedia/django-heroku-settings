from __future__ import unicode_literals

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_required_env_var(name):
    """ Get an environment variable or throw an error if it's missing. """
    result = os.getenv(name)
    if result is None:
        raise Exception("Environment variable %s is required" % name)
    return result



## -------- Security ------------ ##

SECRET_KEY = get_required_env_var("SECRET_KEY")

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

APP_ENVIRONMENT = get_required_env_var('APP_ENV', 'LOCAL')

DEBUG = {'PROD': False, 'CIRCLE_CI': True, 'LOCAL': True}[APP_ENVIRONMENT]

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
# Add your custom domain name here: 'mydjangoapp.com' or '.mydjangoapp.com' if you have subdomains
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.herokuapp.com']


## -------- Templates ------------ ##

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'my_django_app/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                # from https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



## -------- Applications & Middlewares ------------ ##

INSTALLED_APPS = (
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # django apps provided by libraries; add ones you need
    'haystack',

    # Your custom app(s) here
    'my_django_app',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'my_django_app.urls'

WSGI_APPLICATION = 'my_django_app.wsgi.application'

# this is the default setting but let's be explicit
# django will (try to) redirect from url /somewhere to /somewhere/ automatically
APPEND_SLASH = True


## -------- Database ------------ ##

# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Parse database configuration from $DATABASE_URL environment variable
import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}



## -------- Logging ------------ ##

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'my_django_app': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING'
    }
}



## -------- Internationalization ------------ ##

# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True



## -------- Static files ------------ ##

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'



## -------- Search ------------ ##

# use ElasticSearch with Bonsai and Haystack for full text search: https://addons.heroku.com/bonsai

# certifi is needed to support https here
import certifi
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.getenv("BONSAI_URL"),
        'INDEX_NAME': 'haystack',
        'KWARGS': {
            'verify_certs': True,
            'ca_certs': certifi.where(),  # Path to the Certifi bundle.
        }
    },
}



## -------- Cache ------------ ##

# use redis with Redist To Go for caching: https://addons.heroku.com/redistogo

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDISTOGO_URL') + "0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESS_MIN_LEN": 10,
        },
        "KEY_PREFIX": "D_"
    },
    "page": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDISTOGO_URL') + "0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESS_MIN_LEN": 10,
        },
        "KEY_PREFIX": "P_"
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# this setting helps unify page cache timeouts
# use in view decorators: @cache_page(settings.PAGE_CACHE_TIMEOUT, cache="page")
if os.getenv("PAGE_CACHE_TIMEOUT"):
    PAGE_CACHE_TIMEOUT = int(os.getenv("PAGE_CACHE_TIMEOUT"))
else:
    PAGE_CACHE_TIMEOUT = 60 * 9



## -------- 3rd party services ------------ ##

# for Google Analytics
GOOGLE_ANALYTICS_TRACKING_ID = os.getenv("GOOGLE_ANALYTICS_TRACKING_ID")

# AWS if you need it for static files, etc.
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# other 3rd party services
THIRD_PARTY_API_TOKEN = os.getenv("THIRD_PARTY_API_TOKEN")

# Django settings for blacklist project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ("admin", "admin@example.com"),
)

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "%DB_NAME%",                      # Or path to database file if using sqlite3.
        "USER": "%DB_USER%",                      # Not used with sqlite3.
        "PASSWORD": "%DB_PASS%",                  # Not used with sqlite3.
        "HOST": "%DB_HOST%",                      # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/Amsterdam"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = "%DJANGO_ROOT%/media"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# MEDIA_URL = "https://blacklist.as65342.net/media"
MEDIA_URL = "/media/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = "/media/"

# Make this unique, and don"t share it with anybody.
SECRET_KEY = "%DJANGO_SECRET%"

# Cache backend
# CACHE_BACKEND="memcached://127.0.0.1:11211/?timeout=3600"
CACHE_BACKEND="caching.backends.memcached://%CACHE_HOST%:%CACHE_PORT%"
CACHE_COUNT_TIMEOUT=60

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
#     "django.template.loaders.eggs.Loader",
)
TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.request",
	"django.core.context_processors.media",
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pagination.middleware.PaginationMiddleware",
)

ROOT_URLCONF = "urls"
FORCE_SCRIPT_NAME = ""
LOGIN_URL = "/login/"

TEMPLATE_DIRS = (
	"%DJANGO_ROOT%/templates",
)

INSTALLED_APPS = (
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.sites",
	"django.contrib.messages",
	"south",
	"pagination",
	"overview",
	"users",
	"blacklist",
)

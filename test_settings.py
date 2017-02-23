DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':'db.sqlite3'
    }
}

INSTALLED_APPS = (
    'static_version',
)

SECRET_KEY = "secret_key_for_testing"

STATIC_URL = '/static/'

STATIC_VERSION = "1"

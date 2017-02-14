from envs import env

INSTALLED_APPS = (
    'static_version',
)
SECRET_KEY = "secret_key_for_testing"

STATIC_VERSION = env('STATIC_VERSION')

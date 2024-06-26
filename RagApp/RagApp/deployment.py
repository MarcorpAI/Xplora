import os
from .settings import *
from .settings import BASE_DIR



SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = [os.environ["WEBSITE_HOSTNAME"]]

CSRF_TRUSTED_ORIGINS = ["https://"+os.environ["WEBSITE_HOSTNAME"]]

DEBUG = False


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

VENV_PATH = os.path.dirname(BASE_DIR)
STATIC_ROOT = os.path.join(VENV_PATH, 'static_root')

connection_string = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRINGS"]
parameters = {pair.split('=')[0]: pair.split('=')[1] for pair in connection_string.split(' ')}

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parameters['dbname'],
        "HOST": parameters['host'],
        "USER":  parameters['user'],
        "PASSWORD": parameters['password'],
    }
}
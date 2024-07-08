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
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

connection_string = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRINGS"]
parameters = {pair.split('=')[0]: pair.split('=')[1] for pair in connection_string.split(' ')}



TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parameters['dbname'],
        "HOST": parameters['host'],
        "USER":  parameters['user'],
        "PASSWORD": parameters['password'],
    }
}

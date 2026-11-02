import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'samo-za-lokalni-razvoj-spremeni')
DEBUG = os.environ.get('DEBUG', '0') == '1'
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'ucilnica',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'ucilnica.context.uporabniska_vloga',
    ]},
}]
WSGI_APPLICATION = 'config.wsgi.application'
if os.environ.get('USE_SQLITE') == '1':
    # Omogoča preprosto lokalno testiranje brez MariaDB (za razvijalca).
    DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 'NAME':BASE_DIR/'test.sqlite3'}}
else:
    DATABASES = {'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':os.environ.get('DB_NAME','solska'),
        'USER':os.environ.get('DB_USER','dijak'),
        'PASSWORD':os.environ.get('DB_PASSWORD',''),
        'HOST':os.environ.get('DB_HOST','baza'), 'PORT':'3306',
        'OPTIONS':{'charset':'utf8mb4'},
    }}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS':{'min_length':8}},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE='sl'
TIME_ZONE='Europe/Ljubljana'
USE_TZ=True
STATIC_URL='/static/'
STATIC_ROOT=BASE_DIR/'staticfiles'
STATICFILES_DIRS=[BASE_DIR/'static']
STORAGES={
    'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},
    'staticfiles':{'BACKEND':'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
MEDIA_ROOT=BASE_DIR/'media'
MEDIA_URL='/media/'  # naloženih datotek ne strežemo javno: le prek zaščitenih pogledov
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_URL='prijava'
LOGIN_REDIRECT_URL='domov'
LOGOUT_REDIRECT_URL='prijava'
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https')
CSRF_TRUSTED_ORIGINS=[x.strip() for x in os.environ.get('CSRF_TRUSTED_ORIGINS','https://localhost:8443').split(',') if x.strip()]
SESSION_COOKIE_SECURE=os.environ.get('SECURE_COOKIES','0')=='1'
CSRF_COOKIE_SECURE=SESSION_COOKIE_SECURE
FILE_UPLOAD_MAX_MEMORY_SIZE=10*1024*1024
DATA_UPLOAD_MAX_MEMORY_SIZE=25*1024*1024

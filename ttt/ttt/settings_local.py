ALLOWED_HOSTS = ['127.0.0.1']

SECRET_KEY = '' # SET SECRET KEY

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'trepoprod',
        'USER': 'trepoprod',
        'PASSWORD': '',             # SET DATABASE PASSWORD
        'HOST': 'localhost',
        'PORT': '',
    }
}

DEBUG = False
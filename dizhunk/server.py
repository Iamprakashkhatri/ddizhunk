from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  config('IN_DB_NAME'),
        'USER': config('IN_DB_USER'),
        'PASSWORD':  config('IN_DB_PASS'),
        'HOST': config('IN_DB_HOST'),
        'PORT': '5432',
    }
}

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
]

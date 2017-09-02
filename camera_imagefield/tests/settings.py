DEBUG = False

SECRET_KEY = 'test secret key'

INSTALLED_APPS = [
    'camera_imagefield',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
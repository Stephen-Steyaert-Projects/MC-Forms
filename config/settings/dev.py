from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'django-insecure-$2=qf4*y2y6h&+-k7mog(e*%6-3_h7o9sfyf!7%ed!kw+=+!xh'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

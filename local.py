import os
from settings import *


CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'inventory',
        'USER': 'ovunque',
        'PASSWORD': 'qazxc1234',
        'HOST': '',
        'PORT': '3306',
        'TIME_ZONE': 'Asia/Kolkata'
    }
}

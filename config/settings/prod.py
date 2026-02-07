from .base import *

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS')

import hashlib
import random

BASE_DIR='/usr/local'
LOG_DIR='/var/log/blacklist'
HTTP_USER='www-data'
HTTP_HOST='www-data'

DB_SERVER_USER='postgres'
DB_SERVER_GROUP='postgres'
DB_HOST='localhost'
DB_NAME='blacklist'
DB_USER='blacklist'
DB_PASS='blacklist'

CACHE_HOST='127.0.0.1'
CACHE_PORT='11211'

DJANGO_ROOT='%s/blacklist/django-blacklist' % BASE_DIR
DJANGO_SECRET=hashlib.sha512(str(random.random())).hexdigest()

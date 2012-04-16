
import hashlib
import random

BASE_DIR='/usr/local'
LOG_DIR='/var/log/blacklist'
HTTP_USER='www-data'
HTTP_HOST='www-data'

REPORTER_USERNAME='admin'
REPORTER_PASSWORD='blacklist'
REPORTER_PSK='blacklist'

BROKER_URL='tcp://127.0.0.1:5580'

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
DJANGO_PAGES_PER_VIEW=25
DJANGO_KEYSTORE_PSK='blacklist'
DJANGO_MULTIPLIER='3600'

BROKER_ROOT='%s/blacklist/bl-broker' % BASE_DIR
SYSLOG_ROOT='%s/blacklist/bl-syslog' % BASE_DIR
BGP_ROOT='%s/blacklist/bl-bgp' % BASE_DIR

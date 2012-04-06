#!/bin/sh

cd /www/blacklist/app
su - _postgresql -c 'dropdb blacklist'
su - _postgresql -c 'createdb -EUTF8 -Oblacklist blacklist'
python manage.py syncdb


from __future__     import with_statement
from fabric.api     import local, run, cd, settings

import os

import defaults

devel_host = 'blacklist-dev'
devel_user = 'root'

templated_scripts = [
    'django-blacklist/settings.py',
    'django-blacklist/scripts/blacklist-launcher.sh',
    'django-blacklist/scripts/registry-mgmt/import_registry_data.py',
]

template_tags = [
    'BASE_DIR',
    'LOG_DIR',
    'HTTP_USER',
    'HTTP_HOST',
    'DB_SERVER_USER',
    'DB_SERVER_GROUP',
    'DB_HOST',
    'DB_NAME',
    'DB_USER',
    'DB_PASS',
    'CACHE_HOST',
    'CACHE_PORT',
    'DJANGO_ROOT',
    'DJANGO_SECRET',
]

## Installation related
def sync(remote=devel_host, remote_user=devel_user):
    cwd = os.getcwd()
    local('rsync -avl --progress --exclude \'*.pyc\' --exclude \'*.swp\'' \
        ' --exclude \'*/build*\' %s %s@%s:%s' % \
        (cwd, remote_user, remote, defaults.BASE_DIR))

def prepare_environment(remote=devel_host, remote_user=devel_user):
    with settings(host_string=remote, user=remote_user):
        run('install -d -o root -g www-data -m 0770 %s' % defaults.LOG_DIR)

def prepare_scripts(remote=devel_host, remote_user=devel_user):
    with settings(host_string=remote, user=remote_user):
        with cd('%s/blacklist' % defaults.BASE_DIR):
            sed_parameters = ''
            for script in templated_scripts:
                for tag in template_tags:
                    sed_parameters += ' -e \'s,%%%s%%,%s,g\'' % \
                        (tag, eval('defaults.%s' % tag))
                run('sed -i%s %s' % (sed_parameters, script))
                run('rm -f %se' % script)

def prepare_database(remote=devel_host, remote_user=devel_user):
    with settings(host_string=remote, user=remote_user):
        has_database = int(run('su - %s -c \'psql -l | grep -c %s\' || true' \
            % (defaults.DB_SERVER_USER, defaults.DB_NAME)))
        has_user = int(run('su - %s ' % defaults.DB_SERVER_USER +
            '-c \'echo \\\\\du | psql\' | ' +
            'grep -c %s || true' % defaults.DB_USER))
        if has_database != 0:
            run('su - %s -c \'dropdb %s\'' % \
                (defaults.DB_SERVER_USER, defaults.DB_NAME))
        if has_user != 0:
            run('su - %s -c \'dropuser %s\'' % \
                (defaults.DB_SERVER_USER, defaults.DB_USER))
        run('su - %s -c \'createuser -DERS %s\'' % \
            (defaults.DB_SERVER_USER, defaults.DB_USER))
        run('echo \"ALTER USER %s WITH PASSWORD \'%s\'\" | ' % \
            (defaults.DB_USER, defaults.DB_PASS) + \
            'su - %s -c \'psql -d template1 -U %s\'' % \
            (defaults.DB_SERVER_USER, defaults.DB_SERVER_USER))
        run('su - %s -c \'createdb -O %s %s\'' % \
            (defaults.DB_SERVER_USER, defaults.DB_USER, defaults.DB_NAME))
        with cd(defaults.DJANGO_ROOT):
            run('python manage.py syncdb --noinput')
            run('python manage.py migrate')

def import_registry_data(remote=devel_host, remote_user=devel_user):
    with settings(host_string=remote, user=remote_user):
        with cd('%s/scripts/registry-mgmt' % defaults.DJANGO_ROOT):
            run('./import_registry_data.py')

## Testing related
def test_django_blacklist(remote=devel_host, remote_user=devel_user):
    with settings(host_string=remote, user=remote_user):
        with cd('%s/blacklist' % defaults.BASE_DIR):
            run('./django-blacklist/scripts/blacklist-launcher.sh start')
            run('./django-blacklist/scripts/blacklist-launcher.sh stop')

## Top-level functions
def test(remote=devel_host, remote_user=devel_user):
    sync(remote, remote_user)
    prepare_environment(remote, remote_user)
    prepare_scripts(remote, remote_user)
    prepare_database(remote, remote_user)
    import_registry_data(remote, remote_user)
    # test_django_blacklist(remote, remote_user)

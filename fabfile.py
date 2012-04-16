
from __future__     import with_statement
from fabric.api     import local, run, cd, settings, put

import os

import defaults

devel_host = 'blacklist-dev'
devel_user = 'root'

templated_scripts = [
    'bl-broker/bin/bl-broker',
    'bl-syslog/conf/bl-syslog.conf',
    'django-blacklist/settings.py',
    'django-blacklist/scripts/config-cli.py',
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
    'REPORTER_USERNAME',
    'REPORTER_PASSWORD',
    'REPORTER_PSK',
]

## Installation related
def sync(remote=devel_host, remote_user=devel_user):
    cwd = os.getcwd()
    local('rsync -avl --progress --exclude \'*.pyc\' --exclude \'*.swp\'' \
        ' --exclude \'*/build*\' %s %s@%s:%s' % \
        (cwd, remote_user, remote, defaults.BASE_DIR))

def prepare_environment(remote=devel_host, remote_user=devel_user):
    with settings(host_string=remote, user=remote_user):
        run('id blacklist >/dev/null 2>&1 || ' \
            'useradd -r -s /usr/sbin/nologin blacklist')
        run('install -d -o root -g root -m 0555 /var/empty')
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

def prepare_broker(remote=devel_host, remote_user=devel_user):
    with settings(host_string=remote, user=remote_user):
        with cd(defaults.BROKER_ROOT):
            run('python setup.py install')
        put('bl-broker/conf/bl-broker.supervisor.conf', \
            '/etc/supervisor/conf.d/bl-broker.conf')
        run('supervisorctl reread')
        run('supervisorctl add bl-broker')

def prepare_syslog(remote=devel_host, remote_user=devel_user):
    with settings(host_string=remote, user=remote_user):
        with cd(defaults.SYSLOG_ROOT):
            run('python setup.py install')
        put('bl-syslog/conf/bl-syslog.supervisor.conf', \
            '/etc/supervisor/conf.d/bl-syslog.conf')
        run('supervisorctl reread')
        run('supervisorctl add bl-syslog')

def prepare_bgp(remote=devel_host, remote_user=devel_user):
    with settings(host_string=remote, user=remote_user):
        with cd(defaults.BGP_ROOT):
            run('python setup.py install')
        put('bl-bgp/conf/bl-bgp.supervisor.conf', \
            '/etc/supervisor/conf.d/bl-bgp.conf')
        run('supervisorctl reread')
        run('supervisorctl add bl-bgp')

def prepare_django_config(remote=devel_host, remote_user=devel_user):
    with settings(host_string=remote, user=remote_user):
        config_cli = '%s/scripts/config-cli.py' % defaults.DJANGO_ROOT
        run('%s set blacklist.country.pages_per_view %s' % \
            (config_cli, defaults.DJANGO_PAGES_PER_VIEW))
        run('%s set blacklist.keystore.psk %s' % \
            (config_cli, defaults.DJANGO_KEYSTORE_PSK))
        run('%s set blacklist.multiplier %s' % \
            (config_cli, defaults.DJANGO_MULTIPLIER))
        run('%s set blacklist.api.psk %s' % (config_cli, defaults.REPORTER_PSK))
        run('%s set blacklist.broker %s' % (config_cli, defaults.BROKER_URL))

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

def run_django_devserver(remote=devel_host, remote_user=devel_user):           
    with settings(host_string=remote, user=remote_user):
        with cd(defaults.DJANGO_ROOT):
            run('python manage.py runserver 192.168.100.10:8000 || true')

## Top-level functions
def deploy(remote=devel_host, remote_user=devel_user, rebuild_db=False):
    sync(remote, remote_user)
    prepare_environment(remote, remote_user)
    prepare_scripts(remote, remote_user)
    if rebuild_db:
        prepare_database(remote, remote_user)
        import_registry_data(remote, remote_user)
    #prepare_broker(remote, remote_user)
    #prepare_syslog(remote, remote_user)
    #prepare_bgp(remote, remote_user)
    prepare_django_config(remote, remote_user)
    # test_django_blacklist(remote, remote_user)
    # run_django_devserver(remote, remote_user)

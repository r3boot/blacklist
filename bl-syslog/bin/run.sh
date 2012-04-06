#!/bin/sh

cd /projects/bl-syslog
exec /projects/bl-syslog/bin/bl-syslog > /var/log/blacklist/bl-syslog.log 2>&1

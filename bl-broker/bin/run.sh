#!/bin/sh

cd /projects/bl-broker
exec /projects/bl-broker/bin/bl-broker > /var/log/blacklist/bl-broker.log 2>&1

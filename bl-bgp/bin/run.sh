#!/bin/sh

cd /projects/bl-bgp
exec /projects/bl-bgp/bin/bl-bgp > /var/log/blacklist/bl-bgp.log 2>&1

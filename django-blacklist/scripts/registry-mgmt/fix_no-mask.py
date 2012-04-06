#!/usr/bin/env python

import datetime
import os
import re
import sys
import time
import urllib2

sys.path.append("/www/blacklist/app")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from django.db					import transaction, reset_queries
from blacklist.common.ipcalc	import IPCalc
from blacklist.common.netdata	import NetData
from blacklist.models			import *

ipcalc = IPCalc()

error_dir = "/projects/registry-mgmt/errors"

if __name__ == "__main__":
	for rir in ["ARIN", "RIPE", "AfriNIC", "APNIC", "LACNIC"]:
		for l in open("%s/%s-no-mask.txt" % (error_dir, rir), "r").readlines():
			l = l.strip()
			(net, num_ips) = l.split("|")
			print "%s(%s): %s" % (net, num_ips, len(ipcalc.aggregates(ipcalc.dqtoi(net), int(num_ips), [])))
	#print ipcalc.aggregates(ipcalc.dqtoi("196.13.138.0"), 7419)

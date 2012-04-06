#!/usr/bin/env python

import datetime
import os
import re
import sys
import urllib2

sys.path.append("/www/noc.as65342.net/project")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from django.db			import transaction, reset_queries
from r4ck.blacklist.models	import *

iana_asnums = "http://www.iana.org/assignments/as-numbers/as-numbers.txt"

def fetch_txt():
	try:
		return urllib2.urlopen(iana_asnums).readlines()
	except urllib2.HTTPError:
		print "Failed to retrieve txt data"
		sys.exit(1)

def create_registries():
	result = {}
	registries = [
		["ARIN", "whois.arin.net"],
		["RIPE", "whois.ripe.net"],
		["APNIC", "whois.lacnic.net"],
		["LACNIC", "whois.lacnic.net"],
		["AfriNIC", "whois.afrinic.net"],
	]
	for rir in registries:
		r = RIR(name=rir[0], whois=rir[1])
		r.save()
		result[rir[0]] = r
	print "Added %s registries" % (len(registries))
	return result

@transaction.commit_manually
def import_iana_data(rirs):
	for line in fetch_txt():
		if "Assigned by" in line:
			t = line.split()
			asnum = t[0]
			rir = rirs[t[3]]
			print "asnum: %s; rir: %s" % (asnum, rir)
			if "-" in asnum:
				t = asnum.split("-")
				asnum_list = range(int(t[0]), int(t[1])+1)
			else: asnum_list = [int(asnum)]
			for asn in asnum_list:
				asn_reg = ASNumRegistry(asnum=asn, rir=rir)
				asn_reg.save()
	transaction.commit()

if __name__ == "__main__":
	rirs = create_registries()
	import_iana_data(rirs)

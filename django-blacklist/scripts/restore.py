#!/usr/bin/env python

from cPickle	import loads
from os		import environ
from sys	import path, argv, exit, stdout
from pprint	import pprint

path.append("/www/blacklist/app")
environ["DJANGO_SETTINGS_MODULE"] = "settings"

basedir = "/www/blacklist/app/backup"

from blacklist.common.config			import Config
from blacklist.middleware.country		import Country
from blacklist.middleware.rir			import RIR
from blacklist.middleware.asnum			import ASNum
from blacklist.middleware.subnet		import Subnet
from blacklist.middleware.whitelisting	import WhiteListing
from blacklist.middleware.peering		import Peering
from blacklist.middleware.rule			import Rule
from blacklist.middleware.duration		import Duration
from blacklist.middleware.listing		import Listing
from blacklist.middleware.historylisting	import HistoryListing

config = Config()
asnum = ASNum()
country = Country()
rir = RIR()
subnet = Subnet()
whitelisting = WhiteListing()
peering = Peering()
rule = Rule()
duration = Duration()
listing = Listing()
historylisting = HistoryListing()

def log(msg):
	stdout.write(msg)
	stdout.flush()

def get_data(item):
	result = []
	fname = "%s/r4ck-blacklist-%s.csv" % (basedir, item)
	counter = 0
	data = "".join(open(fname, "r").readlines())
	for entry in data.split("<<\n"):
		if entry == "": continue
		entry = entry.strip()
		entry = entry.split("||")
		result.append(entry)
	return result

def restore_config(data):
	log("Restoring config: ")
	for entry in data:
		if entry[0] == "": continue
		config[entry[0]] = entry[1]
		log(".")
	print "done!"

def restore_countries(data):
	log("Restoring countries (%s): "  % (len(data)))
	(t, n, f) = country.bulk_import(data)
	log("%s seconds, %s failed\n" % (t, n))
	if n > 0: pprint(f)

def restore_rirs(data):
	log("Restoring RIRs (%s): "  % (len(data)))
	(t, n, f) = rir.bulk_import(data)
	log("%s seconds, %s failed\n" % (t, n))
	if n > 0: pprint(f)

def restore_asnums(data):
	log("Restoring asnums (%s): "  % (len(data)))
	(t, n, f) = asnum.bulk_import(data)
	log("%s seconds, %s failed\n" % (t, n))
	if n > 0: pprint(f)

def restore_subnets(data):
	log("Restoring subnet (%s): "  % (len(data)))
	(t, n, f) = subnet.bulk_import(data)
	log("%s seconds, %s failed\n" % (t, n))
	if n > 0: pprint(f)

def restore_whitelistings(data):
	log("Restoring whitelistings (%s): "  % (len(data)))
	(t, n, f) = whitelisting.bulk_import(data)
	log("%s seconds, %s failed\n" % (t, n))
	if n > 0: pprint(f)

def restore_peerings(data):
	log("Restoring peerings (%s): " % (len(data)))
	(t, n, f) = peering.bulk_import(data)
	log("%s seconds, %s failed\n" % (t, n))
	if n > 0: pprint(f)

def restore_rules(data):
	log("Restoring rules (%s): " % (len(data)))
	(t, n, f) = rule.bulk_import(data)
	log("%s seconds, %s failed\n" % (t, n))
	if n > 0: pprint(f)

def restore_listings(data):
	log("Restoring listings (%s): " % (len(data)))
	(t, n, f) = listing.bulk_import(data)
	log("%s seconds, %s failed\n" % (t, n))
	if n > 0: pprint(f)

def restore_durations(data):
	log("Restoring durations (%s): " % (len(data)))
	(t, n, f) = duration.bulk_import(data)
	log("%s seconds, %s failed\n" % (t, n))
	if n > 0: pprint(f)

def restore_historylistings(data):
	log("Restoring historic listings (%s): " % (len(data)))
	(t, n, f) = historylisting.bulk_import(data)
	log("%s seconds, %s failed\n" % (t, n))
	if n > 0: pprint(f)

if __name__ == "__main__":
	restore_config(get_data("config"))
	#restore_whitelistings(get_data("whitelist"))
	#restore_peerings(get_data("peering"))
	restore_rules(get_data("rules"))

#!/usr/bin/env python

from os		import environ
from sys	import exit
from sys	import path

path.append("/www/blacklist/app")
environ["DJANGO_SETTINGS_MODULE"] = "settings"

from commands			import getoutput

from blacklist.middleware.user		import *
from blacklist.middleware.whitelist	import *
from blacklist.middleware.peering		import *
from blacklist.middleware.registry		import *

from registry.middleware.network		import *
from registry.middleware.host		import *
from registry.middleware.location		import *

from dns.middleware.view			import *
from dns.middleware.domain			import *
from dns.middleware.record			import *

from scripts.data				import *
from scripts.import_countrycodes		import *
from scripts.import_iana_data			import *

def quitmsg(msg):
	print msg
	#exit(1)

def rebuild_db():
	print getoutput("python /www/blacklist/project/manage.py syncdb --noinput")

def import_hwsw_data():
	print getoutput("/usr/local/share/scripts/import_hwsw_data.py")

def repopulate_db():
	#print "Repopulating users (%s)" % (len(users))
	#for u in users:
	#	(result, data) = create_user(None, u[0], u[1], u[4], u[2], u[3], True)
	#	if not result: quitmsg(data)
	#(result, data) = get_user(None, "r3boot")
	if result: admin_user = data
	else: quitmsg(data)

	print "Repopulating whitelist (%s)" % (len(whitelist))
	for w in whitelist:
		(result, data) = create_whitelist_entry(w[0], w[1], admin_user)
		if not result: quitmsg(data)

	print "Repopulating peerings (%s)" % (len(peerings))
	for p in peerings:
		(result, data) = create_bgp_peering(p[0], p[1], p[2], admin_user)
		if not result: quitmsg(data)


	print "Repopulating locations (%s)" % (len(locations))
	for l in locations:
		(result, data) = create_location(l[0], l[1], admin_user)
		if not result: quitmsg(data)

	print "Repopulating VRFs (%s)" % (len(vrfs))
	for v in vrfs:
		(result, data) = create_vrf(v[0], v[1], admin_user)
		if not result: quitmsg(data)

	print "Repopulating asnums (%s)" % (len(asnums))
	for a in asnums:
		(result, data) = create_asnum(a[0], a[1], admin_user)
		if not result: quitmsg(data)

	print "Repopulating supernets (%s)" % (len(supernets))
	for s in supernets:
		(result, vrf) = get_vrf(s[3])
		if not result: quitmsg(vrf)
		(result, data) = create_network(s[0], s[1], "supernet", vrf, admin_user)
		if not result: quitmsg(data)

	print "Repopulating networks (%s)" % (len(networks))
	(result, vrf) = get_vrf("AS65342")
	if not result: quitmsg(vrf)
	for n in networks:
		(result, data) = create_network(n[0], n[1], n[2], vrf, admin_user)
		if not result: quitmsg(data)

	print "Repopulating network profiles (%s)" % (len(network_profiles))
	for p in network_profiles:
		(result, subnet) = get_network(p[0], None)
		if not result: quitmsg(subnet)
		(result, data) = create_network_profile(subnet)
		if not result: quitmsg(data)

	print "Repopulating network-asnums (%s)" % (len(network_asnums))
	for s in network_asnums:
		(result, vrf) = get_vrf(s[2])
		if not result: quitmsg(vrf)
		(result, subnet) = get_network(s[0], vrf)
		if not result: quitmsg(subnet)
		(result, asnum) = get_asnum(s[1])
		if not result: quitmsg(asnum)
		(result, data) = create_network_asnum(subnet, asnum)
		if not result: quitmsg(data)

	print "Repopulating hosts (%s)" % (len(hosts))
	for h in hosts:
		(result, data) = create_host(h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], admin_user)
		if not result: quitmsg(data)

	print "Repopulating interfaces (%s)" % (len(interfaces))
	for i in interfaces:
		(result, data) = create_interface(i[0], i[1], i[2], i[3], i[4])
		if not result: quitmsg(data)

	print "Repopulating ips (%s)" % (len(ips))
	for i in ips:
		(result, data) = create_ip_address(i[0], i[1], i[2], admin_user)
		if not result: quitmsg(data)

	print "Repopulating views (%s)" % (len(views))
	for v in views:
		(result, data) = create_view(v)
		if not result: quitmsg(data)

def import_countrycodes():
	print "Importing countrycodes (%s)" % (len(countries))
	for country in countries:
		create_countrycode(country[0], country[1])

def import_rir_data():
	print "Importing registries"
	rirs = create_registries()
	print "Creating ASNum registry"
	import_iana_data(rirs)

def import_config():
	print "Rebuilding config (%s)" % (len(config))
	cfg = Config()
	for c in config:
		cfg[c[0]] = c[1]

if __name__ == "__main__":
	#rebuild_db()
	#import_hwsw_data()
	import_config()
	import_countrycodes()
	import_rir_data()
	repopulate_db()

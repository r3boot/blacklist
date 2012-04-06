#!/usr/bin/env python

import socket
import sys
import os

sys.path.append("/www/blacklist/app")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from blacklist.middleware.listing		import Listing
from blacklist.middleware.whitelisting	import WhiteListing

listing = Listing()
whitelisting = WhiteListing()

def help():
	print "Usage: %s (listing|whitelisting) (add|del|list) [<value>]" % (os.path.basename(sys.argv[0]))
	print ""
	print "Examples:"
	print "* listing add 192.0.2.1 reason someuser"
	print "* listing add 192.0.2.0/24 reason someuser"
	print "* listing del 192.0.2.1"
	print "* listing list"
	print "* whitelisting add 192.0.2.1 host.example.com someuser"
	print "* whitelisting add 192.0.2.0/24 net.example.com someuser"
	print "* whitelisting del 192.0.2.1"
	print "* whitelisting list"
	sys.exit(1)

if __name__ == "__main__":
	if not len(sys.argv) in range(3,7):
		help()

	if not sys.argv[1] in ["listing", "whitelisting"]:
		help()

	if not sys.argv[2] in ["add", "del", "list"]:
		help()

	if sys.argv[1] == "listing":
		if sys.argv[2] == "add":
			if len(sys.argv) != 6:
				help()
			(result, listing) = listing.add(
				ip=sys.argv[3],
				reason=sys.argv[4],
				sensor="bl-cli",
				sensor_host=socket.gethostname().split(".")[0],
				reporter=sys.argv[5],
			)
			if result:
				print "ok"
			else:
				print listing
		elif sys.argv[2] == "del":
			(result, listing) = listing.delete(ip=sys.argv[3])
			print listing
		elif sys.argv[2] == "list":
			(result, listings) = listing.all()
			if result:
				if len(listings) == 0:
					print "No listings found"
				else:
					for listing in listings:
						print "%s\t%s" % (listing.ip, listing.reason)
			else:
				print listings
	elif sys.argv[1] == "whitelisting":
		if sys.argv[2] == "add":
			if len(sys.argv) != 6:
				help()
			(result, listing) = whitelisting.add(
				ip=sys.argv[3],
				hostname=sys.argv[4],
				user=sys.argv[5],
			)
			if result:
				print "ok"
			else:
				print listing
		elif sys.argv[2] == "del":
			(result, listing) = whitelisting.delete(ip=sys.argv[3])
			print listing
		elif sys.argv[2] == "list":
			(result, listings) = whitelisting.all()
			if result:
				if len(listings) == 0:
					print "No listings found"
				else:
					for listing in listings:
						print "%s\t%s" % (listing.ip, listing.hostname)
			else:
				print listings

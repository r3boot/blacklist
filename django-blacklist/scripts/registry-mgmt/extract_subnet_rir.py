#!/usr/bin/env python

import sys
import os

sys.path.append("/www/blacklist/app")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from blacklist.common.ipcalc	import IPCalc

ipcalc = IPCalc()

cache_dir = "/www/blacklist/app/scripts/registry-mgmt/cache"
output_dir = "/www/blacklist/app/blacklist/migrations/data"

if __name__ == "__main__":
	out = open("%s/subnet-to-rir.txt" % (output_dir), "w")
	for rir in ["ARIN", "RIPE", "AfriNIC", "APNIC", "LACNIC"]:
		for line in open("%s/%s.txt" % (cache_dir, rir), "r").readlines():
			if line.startswith("#"):
				continue
			elif line.endswith("summary\n"):
				continue
			t = line.split("|")
			if not t[2] in ["ipv4", "ipv6"]:
				continue

			if "." in t[3]:
				af = 4
			else:
				af = 6

			no_mask = False
			if af == 4:
				try:
					mask = ipcalc.iptobit[int(t[4])]
				except KeyError:
					no_mask = True
			else:
				mask = int(t[4])

			if not no_mask:
				out.write("%s|%s\n" % (ipcalc.dqtoi(t[3]), rir))
			else:
				if af == 4:
					for net in ipcalc.aggregates(ipcalc.dqtoi(t[3]), int(t[4]), []):
						out.write("%s|%s\n" % (net[0], rir))

	out.close()

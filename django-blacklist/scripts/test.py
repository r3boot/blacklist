#!/usr/bin/env python

import sys
import os.path
import os

sys.path.append("/www/blacklist/app")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from blacklist.common.search		import Search
from blacklist.middleware.subnet	import Subnet

if __name__ == "__main__":
	s = Search(
		model=Subnet(),
		fields={
			"subnet":		"subnet",
			"mask":			"mask",
			"last": 		"last",
			"provider":		"asnum__name",
			"af":			"af",
			"code":			"country__code",
			"country":		"country__name",
			"rir":			"rir__name",
			"regdate":		"regdate",
			"listed":		"listed",
			"whitelisted":	"whitelisted",
		}
	)
	print s.find("subnet=213.154.229.25 or rir=afrinic")

#!/usr/bin/env python

from os  import environ, walk, chdir, getcwd
from sys import exit, path
path.append("/www/noc.as65342.net/project")
environ["DJANGO_SETTINGS_MODULE"] = "settings"

import unittest

test_dir = "/usr/local/share/r4ck/tests"
units = ["common", "registry", "utils"]

if __name__ == "__main__":
	for u in units: path.append("%s/%s" % (test_dir, u))

	from test_config	import TestConfig
	from test_ipcalc	import TestIPCalc
	from test_location	import TestLocation
	from test_network	import TestNetwork

	unittest.main()

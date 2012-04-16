#!/usr/bin/env python

import sys
import os.path
import os

sys.path.append("%DJANGO_ROOT%")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from blacklist.common.config	import Config

def help():
	print "Usage: %s (get|set|del|list) <key> [<value>]" % (os.path.basename(sys.argv[0]))
	sys.exit(1)

if __name__ == "__main__":
	if not len(sys.argv) in [2,3,4]: help()
	if not sys.argv[1] in ["get", "set", "del", "list"]: help()

	cfg = Config()
	if sys.argv[1] == "get":
		print "==> Getting %s" % (sys.argv[2])
		print cfg[sys.argv[2]]
	elif sys.argv[1] == "set":
		print "==> Setting %s => %s" % (sys.argv[2], sys.argv[3])
		cfg[sys.argv[2]] = sys.argv[3]
	elif sys.argv[1] == "del":
		del(cfg[sys.argv[2]])
	elif sys.argv[1] == "list":
		for k in cfg.keys():
			print "%s: %s" % (k, cfg[k])

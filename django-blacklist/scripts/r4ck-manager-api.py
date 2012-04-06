#!/usr/bin/env python

import sys
import os.path
import os

sys.path.append("/www/noc.as65342.net/project")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from xmlrpclib	import ServerProxy

from r4ck.config		import Config
from r4ck.utils.encryption	import Encryption

if __name__ == "__main__":
	cfg = Config()
	enc = Encryption(cfg["manager.actions.rpc_key"])
	data = {
		"cmd":	"ca.create_dh_params",
		"args":	"as65342.net",
	}
	srv = ServerProxy("http://10.42.15.11:10800/")
	srv.enqueue(enc.encrypt(data))

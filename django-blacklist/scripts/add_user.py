#!/usr/bin/env python

import sys
import os.path
import os

sys.path.append("/www/noc.as65342.net/project")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from r4ck.blacklist.middleware.user             import *

user = sys.argv[1]
passwd = sys.argv[2]

create_user(None, user, passwd, 'spam@me.com', '', '', True)

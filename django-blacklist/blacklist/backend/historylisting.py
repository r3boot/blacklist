from django.db			import transaction, reset_queries
from django.contrib.auth.models	import User
from datetime			import datetime
from time			import mktime,strptime
from socket			import gethostbyname

from blacklist.backend		import BaseBackend
from blacklist			import models
from blacklist.common.netdata		import NetData
from blacklist.common.ipcalc		import IPCalc

class HistoryListing(BaseBackend):
	name = "HistoryListing"
	def __init__(self):
		BaseBackend.__init__(self, models.HistoryListing)
		self.netdata = NetData()
		self.ipcalc = IPCalc()

	def add(self, *args, **kwargs):
		historylisting = models.HistoryListing(**kwargs)
		historylisting.save()
		return (True, historylisting)

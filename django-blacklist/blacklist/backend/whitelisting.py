from django.db		import transaction, reset_queries
from datetime		import datetime
from time			import mktime

from blacklist.backend			import BaseBackend
from blacklist.backend.ip		import IP
from blacklist.common.ipcalc	import IPCalc
from blacklist.common.netdata	import NetData
from blacklist					import models

class WhiteListing(BaseBackend):
	name = "WhiteListing"
	def __init__(self):
		BaseBackend.__init__(self, models.WhiteListing)
		self.ip = IP()
		self.ipcalc = IPCalc()
		self.netdata = NetData()

	def add(self, *args, **kwargs):
		(result, ip) = self.ip.get(ip=kwargs['ip'])
		if not result:
			(result, ip) = self.ip.add(ip=kwargs['ip'])
			if not result:
				return (False, ip)

		(result, listing) = self.get(ip=ip)
		if result:
			return (False, "IP is already whitelisted")

		entry = models.WhiteListing(
			ip=ip,
			hostname=kwargs["hostname"],
		)
		entry.save()
		return (True, entry)

	def delete(self, *args, **kwargs):
		(result, ip) = self.ip.get(ip=kwargs['ip'])
		if not result:
			return (False, ip)
		kwargs['ip'] = ip
		return BaseBackend.delete(self, *args, **kwargs)

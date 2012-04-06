from django.db		import transaction, reset_queries
from datetime		import datetime
from time			import mktime
from socket			import gethostbyname

from blacklist.backend		import BaseBackend
from blacklist.backend.ip	import IP
from blacklist.backend.user	import User
from blacklist				import models
from blacklist.common.netdata			import NetData

class Host(BaseBackend):
	name = "Host"
	def __init__(self):
		BaseBackend.__init__(self, models.Host)
		self.ip = IP()
		self.user = User()

	def add(self, *args, **kwargs):
		(result, host) = self.get(hostname=kwargs['hostname'])
		if result:
			return (True, host)

		if not "ip" in kwargs.keys():
			## TODO: add dns cache
			try:
				kwargs['ip'] = gethostbyname(kwargs['hostname'])
			except:
				return (False, "gethostbyname failed for %s" % (kwargs['hostname']))

		(result, ip) = self.ip.get(ip=kwargs['ip'])
		if not result:
			(result, ip) = self.ip.add(ip=kwargs['ip'])
			if not result:
				return (False, ip)

		(result, user) = self.user.get(username=kwargs['user'])
		if not result:
			(result, user) = self.user.add(username=kwargs['user'])
			if not result:
				return (False, user)

		host = models.Host(
			hostname=kwargs['hostname'],
			ip=ip,
			owner=user,
		)
		host.save()
		return (True, host)

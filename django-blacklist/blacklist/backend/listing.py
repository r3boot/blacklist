from django.db					import transaction, reset_queries
from django.contrib.auth.models	import User
from datetime					import datetime
from time						import mktime,strptime
from socket						import gethostbyname

from blacklist.backend					import BaseBackend
from blacklist.backend.ip				import IP
from blacklist.backend.sensor			import Sensor
from blacklist.backend.host				import Host
from blacklist.backend.reason			import Reason
from blacklist.backend.duration			import Duration
from blacklist.backend.user				import User
from blacklist.backend.historylisting	import HistoryListing
from blacklist							import models
from blacklist.common.config			import Config
from blacklist.common.ipcalc			import IPCalc

class Listing(BaseBackend):
	name = "Listing"
	def __init__(self):
		BaseBackend.__init__(self, models.Listing)
		self.ip = IP()
		self.sensor = Sensor()
		self.host = Host()
		self.reason = Reason()
		self.duration = Duration()
		self.user = User()
		self.historylisting = HistoryListing()
		self.config = Config()
		self.ipcalc = IPCalc()

	def add(self, *args, **kwargs):
		(result, ip) = self.ip.get(ip=kwargs['ip'])
		if not result:
			(result, ip) = self.ip.add(ip=kwargs['ip'])
			if not result:
				return (False, ip)

		(result, listing) = self.get(ip=ip)
		if result:
			return (False, "IP is already blacklisted")

		(result, sensor) = self.sensor.get(name=kwargs['sensor'])
		if not result:
			(result, sensor) = self.sensor.add(name=kwargs['sensor'])
			if not result:
				return (False, sensor)

		(result, sensor_host) = self.host.get(hostname=kwargs['sensor_host'])
		if not result:
			(result, sensor_host) = self.host.add(hostname=kwargs['sensor_host'], user=kwargs['reporter'])
			if not result:
				return (False, sensor_host)

		(result, reason) = self.reason.get(reason=kwargs['reason'], sensor=sensor)
		if not result:
			(result, reason) = self.reason.add(reason=kwargs['reason'], sensor=sensor)
			if not result:
				return (False, reason)

		(result, user) = self.user.get(username=kwargs['reporter'])
		if not result:
			(result, user) = self.user.add(username=kwargs['reporter'])
			if not result:
				return (False, user)

		(result, historylistings) = self.historylisting.filter(ip=ip)
		if result and len(historylistings) != 0:
			occurrences = len(historylistings)
		else:
			occurrences = 1

		(result, duration) = self.duration.get(duration=occurrences*self.config["blacklist.multiplier"])
		if not result:
			(result, duration) = self.duration.add(duration=occurrences*self.config["blacklist.multiplier"])
			if not result:
				return (False, duration)

		listing = models.Listing(
			ip=ip,
			reason=reason,
			sensor=sensor,
			sensor_host=sensor_host,
			timestamp=datetime.now(),
			duration=duration,
			reporter=user,
		)
		listing.save()

		historylisting = self.historylisting.add(
			ip=ip,
			reason=reason,
			sensor=sensor,
			sensor_host=sensor_host,
			timestamp=listing.timestamp,
			duration=duration,
			reporter=user
		)

		return (True, listing)

	def delete(self, *args, **kwargs):
		try:
			return BaseBackend.delete(self, *args, **kwargs)
		except:
			(result, ip) = self.ip.get(ip=kwargs['ip'])
			if not result:
				return (False, ip)
			kwargs['ip'] = ip
			return BaseBackend.delete(self, *args, **kwargs)

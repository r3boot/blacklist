from django.db		import transaction, reset_queries
from datetime		import datetime
from time			import mktime

from blacklist.backend			import BaseBackend
from blacklist.backend.subnet	import Subnet
from blacklist					import models
from blacklist.common.netdata				import NetData
from blacklist.common.ipcalc				import IPCalc

class IP(BaseBackend):
	name = "IP"
	def __init__(self):
		BaseBackend.__init__(self, models.IP)
		self.netdata = NetData()
		self.ipcalc = IPCalc()
		self.subnet = Subnet()

	def has(self, *args, **kwargs):
		(dq, mask) = self.ipcalc.parse_addr(kwargs['ip'])
		ip = self.ipcalc.dqtoi(dq)
		return BaseBackend.has(self, ip=ip, mask=mask)

	def get(self, *args, **kwargs):
		(dq , mask) = self.ipcalc.parse_addr(kwargs['ip'])
		ip = self.ipcalc.dqtoi(dq)
		return BaseBackend.get(self, *args, ip=ip)

	def add(self, *args, **kwargs):
		af = self.ipcalc.af(kwargs['ip'])
		if not af in [4,6]:
			return (False, "No AF found for %s" % (ip))

		if "/" in kwargs['ip']:
			(ip, mask) = kwargs['ip'].split('/')
			first = self.ipcalc.dqtoi(ip)
			last=first + self.ipcalc.size(kwargs['ip'])
		else:
			ip = kwargs['ip']
			if af == 4:
				mask = 32
			elif af == 6:
				mask = 128
			first = self.ipcalc.dqtoi(ip)
			last = first

		if self.has(ip=ip, mask=mask):
			return (True, self.get(ip=ip, mask=mask))

		try:
			(asn, asn_name, whois_data, net, cc) = self.netdata.get_whois_data(kwargs["ip"])
		except ValueError:
			return (False, "Cannot fetch whois data")

		if net == "0.0.0.0/0":
			net = None
		else:
			if not self.subnet.has(subnet=net):
				(result, net) = self.subnet.add(subnet=net, asn=asn, asn_name=asn_name, whois_data=whois_data, cc=cc)
				if not result:
					return (False, net)
			else:
				(result, net) = self.subnet.get(subnet=net)
				if not result:
					return (False, net)

		ip = models.IP(
			ip=first,
			mask=mask,
			last=last,
			subnet=net,
			af=af
		)
		ip.save()
		return (True, ip)

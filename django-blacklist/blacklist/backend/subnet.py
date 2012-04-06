from django.db		import transaction, reset_queries
from datetime		import datetime
from time			import mktime

from blacklist.backend			import BaseBackend
from blacklist.backend.asnum	import ASNum
from blacklist.backend.country	import Country
from blacklist.backend.rir		import RIR
from blacklist					import models
from blacklist.common.ipcalc	import IPCalc

class Subnet(BaseBackend):
	name = "Subnet"
	def __init__(self):
		BaseBackend.__init__(self, models.Subnet)
		self.ipcalc = IPCalc()
		self.asnum = ASNum()
		self.country = Country()
		self.rir = RIR()

	def has(self, *args, **kwargs):
		if "/" in kwargs['subnet']:
			kwargs['subnet'] = kwargs['subnet'].split("/")[0]
		subnet = self.ipcalc.dqtoi(kwargs['subnet'])
		return BaseBackend.has(self, subnet=subnet)

	def get(self, *args, **kwargs):
		if kwargs.has_key('subnet'):
			if "/" in kwargs['subnet']:
				kwargs['subnet'] = kwargs['subnet'].split("/")[0]
			subnet = self.ipcalc.dqtoi(kwargs['subnet'])
			return BaseBackend.get(self, subnet=subnet)
		else:
			return BaseBackend.get(self, *args, **kwargs)

	def contains(self, *args, **kwargs):
		ip = self.ipcalc.dqtoi(kwargs["ip"])
		net = models.Subnet.objects.filter(subnet__lte=ip).filter(last__gte=ip)
		if net:
			return (True, net)
		else:
			return (False, "No network found for %s" % (kwargs["ip"]))

	def add(self, *args, **kwargs):
		if not "/" in kwargs['subnet']:
			return (False, "%s is not a subnet" % (kwargs['subnet']))

		(net, mask) = kwargs['subnet'].split("/")
		asn = kwargs['asn']
		af = self.ipcalc.af(kwargs['subnet'])

		(result, subnet) = self.get(subnet=net)
		if result:
			return (True, subnet)

		if kwargs['asn'] == 0:
			(result, rir) = self.rir.get(name="Unknown")
			if not result:
				return (False, rir)

		(result, country) = self.country.get(code=kwargs['cc'])
		if not result:
				return (False, country)

		(result, asnum) = self.asnum.get(asnum=kwargs['asn'])
		if not result:
			(result, asnum) = self.asnum.add(asnum=asn, name=kwargs['asn_name'], whois_data=kwargs['whois_data'], country=country, rir=rir)
			if not result:
				return (False, asnum)

		net_first=self.ipcalc.dqtoi(net)
		net_last = net_first + self.ipcalc.bittoip[int(mask)]

		subnet = models.Subnet(
			subnet=net_first,
			last=net_last,
			mask=int(mask),
			asnum=asnum,
			af=af,
			country=country,
			rir=asnum.rir,
			regdate=datetime.now()
		)
		subnet.save()
		return (True, subnet)

	@transaction.commit_manually
	def bulk_import(self, import_data):
		t_start = mktime(datetime.now().timetuple())
		data = []
		failed = []
		num_failed = 0
		for entry in import_data:
			if entry[0] == "":
				num_failed += 1
				failed.append(entry)
				continue
			(net, mask) = entry[0].split("/")
			tmp = {}
			tmp["subnet"] = self.ipcalc.dqtoi(net)
			tmp["mask"] = mask
			tmp["name"] = entry[1]
			try:
				tmp["asnum"] = models.ASNum.objects.filter(name=entry[2])[0]
			except:
				tmp["asnum"] = None
			data.append(tmp)
		for entry in data:
			subnet = models.Subnet(
				subnet=entry["subnet"],
				mask=entry["mask"],
				name=entry["name"],
				asnum=entry["asnum"],
			)
			subnet.save()
		transaction.commit()
		reset_queries()
		t_end = mktime(datetime.now().timetuple())
		return (t_end - t_start, num_failed, failed)

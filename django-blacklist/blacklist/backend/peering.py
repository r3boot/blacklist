from django.db			import transaction, reset_queries
from django.contrib.auth.models	import User
from datetime			import datetime
from time			import mktime

from blacklist.backend		import BaseBackend
from blacklist			import models
from blacklist.common.config		import Config
from blacklist.common.encryption		import Encryption
from blacklist.common.ipcalc		import IPCalc
from blacklist.common.netdata		import NetData

class Peering(BaseBackend):
	name = "Peering"
	def __init__(self):
		BaseBackend.__init__(self, models.Peering)
		self.config = Config()
		self.encryption = Encryption(self.config["blacklist.keystore.psk"])
		self.ipcalc = IPCalc()
		self.netdata = NetData()

	#@transaction.commit_manually
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
			tmp = {}

			try:
				user = User.objects.get(username=entry[3])
			except User.DoesNotExist:
				user = User(username=entry[3])
				user.save()

			try:
				asnum = models.ASNum.objects.get(asnum=entry[1])
			except models.ASNum.DoesNotExist:
				## TODO: fix unknown RIR
				asnum = models.ASNum(
					asnum=entry[1],
					rir=models.RIR.objects.get(name="RIPE")
				)
				asnum.save()

			(asn, asn_name, whois_data, net, cc) = self.netdata.get_whois_data(entry[0])

			try:
				country = models.Country.objects.get(code=cc)
			except models.Country.DoesNotExist:
				country = models.Country(code=cc, name=cc)
				country.save()

			try:
				asnum = models.ASNum.objects.get(asnum=asn)
			except models.ASNum.DoesNotExist:
				asnum = models.ASNum(
					asnum=asnum,
					name=asn_name,
					whois_data=whois_data,
					country=country,
				)
				asnum.save()

			(n, m) = net.split("/")
			try:
				subnet = models.Subnet.objects.get(subnet=self.ipcalc.dqtoi(n))
			except models.Subnet.DoesNotExist:
				subnet = models.Subnet(
					subnet=self.ipcalc.dqtoi(n),
					mask=m,
					name=asn_name,
					asnum=asnum,
				)
				subnet.save()

			try:
				ip = models.IP.objects.get(ip=self.ipcalc.dqtoi(entry[0]))
			except models.IP.DoesNotExist:
				ip = models.IP(
					ip=self.ipcalc.dqtoi(entry[0]),
					subnet=subnet,
				)
				ip.save()

			try:
				peer = models.Host.objects.get(hostname=entry[2])
			except models.Host.DoesNotExist:
				peer = models.Host(
					hostname=entry[2],
					ip=ip,
					owner=user,
				)
				peer.save()

			try:
				key = models.Key.objects.get(name="%s-bgp" % (entry[2]))
			except models.Key.DoesNotExist:
				key = models.Key(
					name="%s-bgp" % (entry[2]),
					data=self.encryption.encrypt(entry[4])
				)
				key.save()

			tmp["peer"] = peer
			tmp["asnum"] = asnum
			tmp["owner"] = user
			tmp["key"] = key
			data.append(tmp)
		for entry in data:
			peering = models.Peering(
				peer=entry["peer"],
				asnum=entry["asnum"],
				user=entry["owner"],
				key=entry["key"]
			)
			peering.save()

		#transaction.commit()
		#reset_queries()
		t_end = mktime(datetime.now().timetuple())
		return (t_end - t_start, num_failed, failed)

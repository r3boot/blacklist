
import sys
import os
sys.path.append("/www/blacklist/app")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

import commands
import dns.resolver

from blacklist.common.ipcalc	import IPCalc
from blacklist.middleware.asnum	import ASNum

class NetData:
	def __init__(self):
		self.ipcalc = IPCalc()
		self.asnum = ASNum()

	def revip(self, ip, af):
		if af == 4:
			t = ip.split(".")
			return "%s.%s.%s.%s" % (t[3], t[2], t[1], t[0])
		elif af == 6:
			ip = ip.split("::")[0].split(":")
			ip.reverse()
			tmp = ""
			for i in ip:
				x = "%04X" % (int(i, 16))
				tmp += x[::-1]
			rev = ""
			for i in range(0, len(tmp)):
				rev += "%s." % (tmp[i])
			return rev[:-1]

	def get_origin(self, ip):
		af = self.ipcalc.af(ip)
		if af == 4:
			query = "%s.origin.asn.cymru.com" % (self.revip(ip, af))
		elif af == 6:
			query = "%s.origin6.asn.cymru.com" % (self.revip(ip, af))
		else:
			return None

		try:
			entry = dns.resolver.query(query, "TXT")
		except:
			return None
		for rdata in entry:
			data = str(rdata).replace("\"", "")
		t = data.split(" | ")
		return [t[0], t[1], t[2]]

	def get_subnet_asnum(self, ip):
		try:
			return self.get_origin(ip)[0].split(" ")[0]
		except:
			return None

	def get_asn_name(self, asn):
		query = "AS%s.asn.cymru.com" % (asn)
		try: entry = dns.resolver.query(query, "TXT")
		except: return "Unknown"
		for rdata in entry:
			data = str(rdata).replace("\"", "")
		try: return data.split(" | ")[4]
		except: return "Unknown"

	def query_whois(self, server, asnum):
		#return commands.getoutput("whois -h %s as%s" % (server, asnum)).split("\n")
		return ""

	def parse_whois_data(self, raw_whois_data):
		rirs = ["APNIC", "LACNIC", "AfriNIC", "RIPE", "ARIN"]
		data = ""
		in_aut_num = False
		in_role = False
		in_person = False
		for line in raw_whois_data:
			if len(line) == 0:
				in_aut_num = False
				in_role = False
				in_person = False
				if len(data) != 0 and data[-2:] != "\n\n": data += "\n"
			elif line.startswith("aut-num:"): in_aut_num = True
			elif line.startswith("ASNumber:"): in_aut_num = True
			elif line.startswith("OrgName:"): in_role = True
			elif line.startswith("OrgTechHandle:"): in_person = True
			elif line.startswith("OrgAbuseHandle:"): in_person = True
			elif line.startswith("role:"):
				is_rir = False
				for rir in rirs:
					if rir in line: is_rir = True
				if not is_rir: in_role = True
			elif line.startswith("person:"): in_person = True
			elif line.startswith("import:"): continue
			elif line.startswith("export:"): continue
			elif line.startswith("default:"): continue
			elif line.startswith("source:"): continue
			elif line.startswith("remarks:"): continue
			elif line.startswith("mp-import:"): continue
			elif line.startswith("mp-export:"): continue
			elif line.startswith("+"): continue
			elif line.startswith("\t"): continue
			elif line.startswith(" "): continue
	
			if in_aut_num:
				data += "%s\n" % (line)
			elif in_role:
				data += "%s\n" % (line)
			elif in_person:
				data += "%s\n" % (line)
		return data

	def get_whois_data(self, ip):
		try:
			(asn, net, country) = self.get_origin(ip)
		except:
			return (0, "UNKNOWN", "Unknown ASN", "0.0.0.0/0", "NL")
		asn_name = self.get_asn_name(asn)
		asn = asn.split()[0]
		(result, asn_obj) = self.asnum.get(asnum=asn)
		if not result:
			return (False, asn_obj)
		raw_whois_data = self.query_whois(asn_obj.rir.whois, asn)
		return (asn, asn_name, self.parse_whois_data(raw_whois_data), net, country)

if __name__ == "__main__":
	netdata = NetData()
	#print netdata.get_whois_data('213.154.229.26')
	print netdata.get_whois_data('10.42.0.2')

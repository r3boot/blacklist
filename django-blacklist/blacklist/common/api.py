
from blacklist.middleware.listing		import Listing
from blacklist.middleware.whitelisting	import WhiteListing
from blacklist.middleware.rule			import Rule
from blacklist.middleware.asnum			import ASNum
from blacklist.middleware.subnet		import Subnet
from blacklist.middleware.rir			import RIR
from blacklist.middleware.country		import Country
from blacklist.middleware.peering		import Peering

class API:
	def __init__(self):
		self.listing = Listing()
		self.whitelisting = WhiteListing()
		self.rule = Rule()
		self.asnum = ASNum()
		self.subnet = Subnet()
		self.rir = RIR()
		self.country = Country()
		self.peering = Peering()

	def add(self, data):
		(result, listing) = self.listing.add(
			ip=data['ip'],
			sensor=data['sensor'],
			sensor_host=data['sensor_host'],
			reason=data['reason'],
			reporter=data['username'],
		)
		return (result, str(listing))

	def get_rules(self):
		rules = {}
		(result, db_rules) = self.rule.all()
		if result:
			for r in db_rules:
				if not rules.has_key(r.sensor.name):
					rules[r.sensor.name] = []
				rules[r.sensor.name].append([r.rule, r.pos_ip, r.pos_reason])
			return (True, rules)
		else:
			return (False, db_rules)

	def get_peerings(self):
		peerings = []
		(result, db_peerings) = self.peering.all()
		if result:
			for p in db_peerings:
				peerings.append({
					"hostname":	p.peer.hostname,
					"ip":		p.peer.ip.ip,
					"af":		p.peer.ip.af,
					"asnum":	p.asnum.asnum,
					"key":		p.key.data,
				})
			return (True, peerings)
		else:
			return (False, db_peerings)

	def get_listings(self):
		listings = []
		(result, db_listings) = self.listing.all()
		if result:
			for l in db_listings:
				listings.append((l.ip.ip, l.ip.last, l.ip.mask, l.ip.af))

		(result, rir_listings) = self.rir.filter(listed=True)
		if result:
			for rir in rir_listings:
				(result, rir_subnets) = self.subnet.filter(rir=rir)
				if result:
					for s in rir_subnets:
						listings.append((s.subnet, s.last, s.mask, s.af))

		(result, country_listings) = self.country.filter(listed=True)
		if result:
			for country in country_listings:
				(result, country_subnets) = self.subnet.filter(country=country)
				if result:
					for s in country_subnets:
						listings.append((s.subnet, s.last, s.mask, s.af))

		(result, provider_listings) = self.asnum.filter(listed=True)
		if result:
			for asnum in provider_listings:
				(result, provider_subnets) = self.subnet.filter(asnum=asnum)
				if result:
					for s in provider_subnets:
						listings.append((s.subnet, s.last, s.mask, s.af))

		(result, subnet_listings) = self.subnet.filter(listed=True)
		if result:
			for s in subnet_listings:
				listings.append((s.subnet, s.last, s.mask, s.af))

		return (True, list(set(listings)))

	def get_whitelistings(self):
		listings = []
		(result, db_listings) = self.whitelisting.all()
		if result:
			for l in db_listings:
				listings.append((l.ip.ip, l.ip.last, l.ip.mask, l.ip.af))

		(result, rir_listings) = self.rir.filter(whitelisted=True)
		if result:
			for rir in rir_listings:
				(result, rir_subnets) = self.subnet.filter(rir=rir)
				if result:
					for s in rir_subnets:
						listings.append((s.subnet, s.last, s.mask, s.af))

		(result, country_listings) = self.country.filter(whitelisted=True)
		if result:
			for country in country_listings:
				(result, country_subnets) = self.subnet.filter(country=country)
				if result:
					for s in country_subnets:
						listings.append((s.subnet, s.last, s.mask, s.af))

		(result, provider_listings) = self.asnum.filter(whitelisted=True)
		if result:
			for asnum in provider_listings:
				(result, provider_subnets) = self.subnet.filter(asnum=asnum)
				if result:
					for s in provider_subnets:
						listings.append((s.subnet, s.last, s.mask, s.af))

		(result, subnet_listings) = self.subnet.filter(whitelisted=True)
		if result:
			for s in subnet_listings:
				listings.append((s.subnet, s.last, s.mask, s.af))

		return (True, list(set(listings)))



from django.db			import models
from django.contrib.auth.models	import User

import caching.base

from blacklist.common.ipcalc		import IPCalc

ipcalc = IPCalc()

class ConfigStore(models.Model):
	key	= models.CharField(max_length=250, unique=True, db_index=True)
	value	= models.TextField()

	def __unicode__(self):
		return self.key

class RIR(models.Model):
	name			= models.CharField(max_length=32, unique=True, db_index=True)
	whois			= models.CharField(max_length=256)
	listed			= models.BooleanField(default=False)
	whitelisted		= models.BooleanField(default=False)
	num_providers	= models.IntegerField(default=0)
	num_subnets		= models.IntegerField(default=0)
	num_listed		= models.IntegerField(default=0)
	num_whitelisted	= models.IntegerField(default=0)
	num_history		= models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class Country(models.Model):
	code		= models.CharField(max_length=2, unique=True, db_index=True)
	name		= models.CharField(max_length=256)
	additional	= models.CharField(max_length=512, blank=True, null=True)
	rir			= models.ForeignKey(RIR)
	listed		= models.BooleanField(default=False)
	whitelisted	= models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering	= ["code"]

class Duration(models.Model):
	duration	= models.IntegerField(unique=True, db_index=True)

	def __unicode__(self):
		return str(self.duration)

class Key(models.Model):
	name	= models.CharField(max_length=250, unique=True, db_index=True)
	data	= models.TextField()

	def __unicode__(self):
		return self.name

class Role(models.Model):
	name	= models.CharField(max_length=250, unique=True, db_index=True)
	view	= models.BooleanField(default=False)
	manage	= models.BooleanField(default=False)
	rpc		= models.BooleanField(default=False)
	admin	= models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

class ASNum(models.Model):
	asnum			= models.CharField(max_length=16, unique=True, db_index=True)
	name			= models.CharField(max_length=2048, blank=True, null=True)
	country 		= models.ForeignKey(Country)
	rir				= models.ForeignKey(RIR)
	regdate			= models.DateTimeField()
	listed			= models.BooleanField(default=False)
	whitelisted		= models.BooleanField(default=False)
	num_subnets		= models.IntegerField(default=0)
	num_listed		= models.IntegerField(default=0)
	num_whitelisted	= models.IntegerField(default=0)
	num_history		= models.IntegerField(default=0)

	class Meta:
		ordering	= ["asnum"]

	def __unicode__(self):
		return str(self.asnum)

class Subnet(models.Model):
	subnet			= models.DecimalField(max_digits=39, decimal_places=0, db_index=True)
	mask			= models.IntegerField(db_index=True)
	last			= models.DecimalField(max_digits=39, decimal_places=0, db_index=True)
	asnum			= models.ForeignKey(ASNum, blank=True, null=True)
	af				= models.IntegerField()
	country			= models.ForeignKey(Country)
	rir				= models.ForeignKey(RIR)
	regdate			= models.DateTimeField()
	listed			= models.BooleanField(default=False)
	whitelisted		= models.BooleanField(default=False)
	num_listed		= models.IntegerField(default=0)
	num_whitelisted	= models.IntegerField(default=0)

	class Meta:
		ordering	= ["subnet"]

	def __unicode__(self):
		return "%s/%s" % (ipcalc.itodq(int(self.subnet), self.af), self.mask)

class IP(models.Model):
	ip			= models.DecimalField(max_digits=39, decimal_places=0, db_index=True)
	mask		= models.IntegerField(db_index=True)
	last		= models.DecimalField(max_digits=39, decimal_places=0, db_index=True)
	subnet		= models.ForeignKey(Subnet, blank=True, null=True)
	af			= models.IntegerField()
	listed		= models.BooleanField(default=False)
	whitelisted	= models.BooleanField(default=False)
	num_listed	= models.IntegerField(default=0)

	def __unicode__(self):
		return ipcalc.itodq(int(self.ip), self.af)

class Host(models.Model):
	hostname	= models.CharField(max_length=512, unique=True, db_index=True)
	ip			= models.ForeignKey(IP)
	owner		= models.ForeignKey(User)

	def __unicode__(self):
		return self.hostname

class Sensor(models.Model):
	name	= models.CharField(max_length=256, unique=True, db_index=True)

	def __unicode__(self):
		return self.name

class Peering(models.Model):
	peer	= models.ForeignKey(Host)
	asnum	= models.ForeignKey(ASNum)
	user	= models.ForeignKey(User)
	key	= models.ForeignKey(Key)

	def __unicode__(self):
		return self.name

class Reason(models.Model):
	reason	= models.CharField(max_length=1024, db_index=True)
	sensor	= models.ForeignKey(Sensor)

	def __unicode__(self):
		return self.reason

class Rule(models.Model):
	rule		= models.TextField()
	sensor		= models.ForeignKey(Sensor)
	pos_ip		= models.IntegerField()
	pos_reason	= models.IntegerField()

	def __unicode__(self):
		return self.name

class Ignore(models.Model):
	ignore	= models.TextField()
	sensor	= models.ForeignKey(Sensor)

	def __unicode__(self):
		return self.name

class Listing(models.Model):
	ip			= models.ForeignKey(IP)
	reason		= models.ForeignKey(Reason)
	sensor		= models.ForeignKey(Sensor)
	sensor_host	= models.ForeignKey(Host)
	timestamp	= models.DateTimeField()
	duration	= models.ForeignKey(Duration)
	reporter	= models.ForeignKey(User)

	def __unicode__(self):
		return str(self.ip)

class HistoryListing(models.Model):
	ip			= models.ForeignKey(IP)
	reason		= models.ForeignKey(Reason)
	sensor		= models.ForeignKey(Sensor)
	sensor_host	= models.ForeignKey(Host)
	timestamp	= models.DateTimeField()
	duration	= models.ForeignKey(Duration)
	reporter	= models.ForeignKey(User)

	def __unicode__(self):
		return self.ip

class WhiteListing(models.Model):
	ip			= models.ForeignKey(IP)
	hostname	= models.CharField(max_length=512)

	def __unicode__(self):
		return self.hostname

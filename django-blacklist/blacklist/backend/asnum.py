
from django.db			import transaction, reset_queries
from datetime			import datetime
from time				import mktime

from blacklist.backend			import BaseBackend
from blacklist.backend.rir		import RIR
from blacklist.backend.country	import Country
from blacklist					import models

class ASNum(BaseBackend):
	name = "ASNum"
	def __init__(self):
		BaseBackend.__init__(self, models.ASNum)
		self.rir = RIR()
		self.country = Country()

	def add(self, *args, **kwargs):
		if isinstance(kwargs['asnum'], int):
			kwargs['asnum'] = str(kwargs['asnum'])

		kwargs['regdate'] = datetime.now()

		if not 'name' in kwargs.keys():
			kwargs['name'] = 'Unknown'

		if not 'country' in kwargs.keys():
			(result, country) = self.country.get(code='EU')
			if not result:
				return (False, country)

		(result, rir) = self.rir.get(name=kwargs['rir'])
		if not result:
			return (False, rir)

		asnum = models.ASNum(
			asnum=kwargs['asnum'],
			name=kwargs['name'],
			country=country,
			rir=rir,
			regdate=kwargs['regdate'],
		)
		asnum.save()
		return (True, asnum)

	@transaction.commit_manually
	def bulk_import(self, import_data):
		t_start = mktime(datetime.now().timetuple())
		data = []
		failed = []
		num_failed = 0
		for entry in import_data:
			tmp = {}
			if entry[0] == "":
				num_failed += 1
				failed.append(entry)
				continue
			
			tmp["asnum"] = entry[0]
			tmp["rir"] = models.RIR.objects.get(name=entry[1])
			data.append(tmp)
		for entry in data:
			asnum = models.ASNum(
				asnum=int(entry["asnum"]),
				rir=entry["rir"],
			)
			asnum.save()
		transaction.commit()
		reset_queries()
		t_end = mktime(datetime.now().timetuple())
		return (t_end - t_start, num_failed, failed)

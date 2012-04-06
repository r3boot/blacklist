from django.db			import transaction, reset_queries
from datetime			import datetime
from time			import mktime

from blacklist.backend		import BaseBackend
from blacklist			import models

class Country(BaseBackend):
	name = "Country"
	def __init__(self):
		BaseBackend.__init__(self, models.Country)

	@transaction.commit_manually
	def bulk_import(self, import_data):
		t_start = mktime(datetime.now().timetuple())
		data = []
		num_failed = 0
		failed = []
		for entry in import_data:
			if entry[0] == "":
				num_failed += 1
				failed.append(entry)
				continue
			if entry[1] == "":
				num_failed += 1
				failed.append(entry)
				continue
			tmp = {}
			tmp["code"] = entry[0]
			tmp["name"] = entry[1].lower()
			data.append(tmp)
		for entry in data:
			country = models.Country(
				code=entry["code"],
				name=entry["name"],
			)
			country.save()
		transaction.commit()
		reset_queries()
		t_end = mktime(datetime.now().timetuple())
		return (t_end - t_start, num_failed, failed)

from django.db		import transaction, reset_queries
from datetime		import datetime
from time		import mktime

from blacklist.backend	import BaseBackend
from blacklist		import models

class Duration(BaseBackend):
	name = "Duration"
	def __init__(self):
		BaseBackend.__init__(self, models.Duration)

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
			tmp = {}
			tmp["duration"] = entry[0]
			tmp["range"] = entry[1]
			data.append(tmp)
		for entry in data:
			duration = models.Duration(
				range=entry["range"],
				duration=entry["duration"],
			)
			duration.save()
		transaction.commit()
		reset_queries()
		t_end = mktime(datetime.now().timetuple())
		return (t_end - t_start, num_failed, failed)

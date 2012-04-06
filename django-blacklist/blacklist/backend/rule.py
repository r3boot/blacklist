from django.db		import transaction, reset_queries
from datetime		import datetime
from time		import mktime

from blacklist.backend			import BaseBackend
from blacklist.backend.sensor	import Sensor
from blacklist					import models

class Rule(BaseBackend):
	name = "Rule"
	def __init__(self):
		BaseBackend.__init__(self, models.Rule)
		self.sensor = Sensor()

	def add(self, *args, **kwargs):
		(result, sensor) = self.sensor.get(name=kwargs["sensor"])
		if not result:
			(result, sensor) = self.sensor.add(name=kwargs["sensor"])
			if not result:
				return (False, sensor)

		(result, rule) = self.get(rule=kwargs["rule"])
		if result:
			return (False, "Rule already exists")

		rule = models.Rule(
			rule=kwargs["rule"],
			sensor=sensor,
			pos_ip=kwargs["pos_ip"],
			pos_reason=kwargs["pos_reason"],
		)
		rule.save()

		return (True, rule)

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
			try:
				sensor = models.Sensor.objects.get(name=entry[0])
			except models.Sensor.DoesNotExist:
				sensor = models.Sensor(name=entry[0])
				sensor.save()

			tmp["sensor"] = sensor
			tmp["rule"] = entry[1]
			tmp["pos_ip"] = entry[2]
			tmp["pos_reason"] = entry[3]
			data.append(tmp)
		for entry in data:
			rule= models.Rule(
				rule=entry["rule"],
				sensor=entry["sensor"],
				pos_ip=entry["pos_ip"],
				pos_reason=entry["pos_reason"],
			)
			rule.save()
		transaction.commit()
		reset_queries()
		t_end = mktime(datetime.now().timetuple())
		return (t_end - t_start, num_failed, failed)

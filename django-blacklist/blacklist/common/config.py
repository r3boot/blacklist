from cPickle		import loads, dumps

from blacklist.models	import ConfigStore

class Config:
	def __typevalue(self, value):
		if isinstance(value, int): return value
		elif isinstance(value, float): return value
		elif isinstance(value, list): return value
		elif isinstance(value, bool): return value
		elif isinstance(value, str):
			try:
				if "." in value: return float(value)
				else: return int(value)
			except:
				if "," in value:
					tmp = []
					for item in value.split(","):
						tmp.append(item.strip())
					return tmp
				else:
					return value
		else: return value

	def __getitem__(self, key):
		try:
			cs_obj = ConfigStore.objects.get(key=key)
			return self.__typevalue(loads(str(cs_obj.value)))
		except:
			return None

	def __setitem__(self, key, value):
		rvalue = self.__typevalue(value)

		try:
			cs_obj = ConfigStore.objects.get(key=key)
			cs_obj.value = dumps(rvalue)
			cs_obj.save()
		except ConfigStore.DoesNotExist:
			cs_obj = ConfigStore(key=key, value=dumps(rvalue))
			cs_obj.save()

	def __delitem__(self, key):
		if self.__getitem__(key):
			cs_obj = ConfigStore.objects.get(key=key)
			cs_obj.delete()

	def keys(self):
		keys = []
		for item in ConfigStore.objects.all():
			keys.append(item.key)
		return keys

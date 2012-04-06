import imp
import sys

class BaseBackend:
	name = "BaseBackend"
	def __init__(self, backend):
		self.backend = backend

	def has(self, *args, **kwargs):
		try:
			self.backend.objects.get(*args, **kwargs)
			return True
		except self.backend.DoesNotExist:
			return False

	def get(self, *args, **kwargs):
		try:
			return (True, self.backend.objects.get(*args, **kwargs))
		except self.backend.DoesNotExist:
			return (False, "%s not found" % (self.name))

	def filter(self, *args, **kwargs):
		return (True, self.backend.objects.filter(*args, **kwargs))

	def all(self):
		return (True, self.backend.objects.all())

	def add(self, *args, **kwargs):
		try:
			db_obj = self.backend(*args, **kwargs)
			db_obj.save()
			return (True, db_obj)
		except:
			return (False, "Failed to add %s entry" % (self.name))

	def delete(self, *args, **kwargs):
		(result, db_obj) = self.get(*args, **kwargs)
		if not result: return (False, db_obj)
		db_obj.delete()
		return (True, "%s removed successfully" % (self.name))

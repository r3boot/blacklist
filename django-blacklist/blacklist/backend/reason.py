from django.db		import transaction, reset_queries
from datetime		import datetime
from time			import mktime

from blacklist.backend			import BaseBackend
from blacklist					import models

class Reason(BaseBackend):
	name = "Reason"
	def __init__(self):
		BaseBackend.__init__(self, models.Reason)

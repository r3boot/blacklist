from django.contrib.auth	import models

from blacklist.backend		import BaseBackend

class User(BaseBackend):
	name = "User"
	def __init__(self):
		BaseBackend.__init__(self, models.User)

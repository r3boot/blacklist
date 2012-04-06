from django.contrib.auth			import models

from blacklist.common.config		import Config
from blacklist.common.encryption	import Encryption
from blacklist.backend				import BaseBackend
from blacklist						import models

class Key(BaseBackend):
	name = "Key"
	def __init__(self):
		BaseBackend.__init__(self, models.Key)
		self.config = Config()
		self.encryption  = Encryption(self.config["blacklist.keystore.psk"])

	def get(self, *args, **kwargs):
		(result, keydata) = BaseBackend.get(self, name=kwargs["name"])
		if result:
			keydata.data = self.encryption.decrypt(keydata.data)
		return (result, keydata)

	def add(self, *args, **kwargs):
		if self.has(name=kwargs["name"]):
			return (False, "Key already exists")

		data = self.encryption.encrypt(kwargs["data"])
		key = models.Key(
			name=kwargs["name"],
			data=data,
		)
		key.save()
		return self.get(name=kwargs["name"])

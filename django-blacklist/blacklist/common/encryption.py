
from Crypto.Cipher import AES
import base64
import cPickle

class Encryption:
	_blocksize = 32
	_padding = "{"

	def __init__(self, psk):
		if psk: self._cipher = AES.new(self._pad(psk))

	def _pad(self, s):
		return s + (self._blocksize - len(s) % self._blocksize) * self._padding

	def decrypt(self, data):
		return cPickle.loads(self._cipher.decrypt(base64.urlsafe_b64decode(data.encode("utf-8")).rstrip(self._padding)))

	def encrypt(self, data):
		return base64.urlsafe_b64encode(self._cipher.encrypt(self._pad(cPickle.dumps(data))))

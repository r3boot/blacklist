
from Crypto.Cipher	import AES
import base64
import cPickle
import datetime
import random
import re
import socket
import time
import threading
import urllib2
import zmq

class API(threading.Thread):
	_blocksize = 32
	_padding = "{"
	_hostname = socket.gethostname()

	def __init__(self, config, server):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.config = config
		self.server = server
		self.cipher = AES.new(self._pad(config["psk"]))

		self.context = zmq.Context()
		self.broker = self.context.socket(zmq.REQ)
		self.broker.connect(config["broker"])

		self.updates = self.context.socket(zmq.SUB)
		self.updates.connect(config["updates"])
		self.updates.setsockopt(zmq.SUBSCRIBE, "update_listings")
		self.updates.setsockopt(zmq.SUBSCRIBE, "update_whitelistings")
		self.updates.setsockopt(zmq.SUBSCRIBE, "update_rules")

	def msg(self, msg):
		print "[API]: %s" % (msg)

	def _pad(self, s):
		return s + (self._blocksize - len(s) % self._blocksize) * self._padding

	def _encrypt(self, data):
		return base64.urlsafe_b64encode(self.cipher.encrypt(self._pad(cPickle.dumps(data))))

	def _decrypt(self, data):
		return cPickle.loads(self.cipher.decrypt(base64.urlsafe_b64decode(data.encode("utf-8")).rstrip(self._padding)))

	def _submit(self, data):
		data['username'] = self.config['username']
		data['password'] = self.config['password']
		data['random'] = random.random()*time.mktime(datetime.datetime.timetuple(datetime.datetime.now()))
		enc = self._encrypt(data)

		self.broker.send(enc)
		response = self._decrypt(self.broker.recv())
		return (response["result"], response["data"])

	def get_listings(self):
		cmd = {"action": "get_listings"}
		return self._submit(cmd)

	def get_whitelistings(self):
		cmd = {"action": "get_whitelistings"}
		return self._submit(cmd)

	def get_rules(self):
		cmd = {"action": "get_rules"}
		return self._submit(cmd)

	def add(self, ip, reason, sensor, sensor_host):
		cmd = {
			"action":		"add",
			"ip":			ip,
			"sensor":		sensor,
			"sensor_host":	sensor_host,
			"reason":		reason,
		}
		return self._submit(cmd)

	def run(self):
		while not self.server.stop:
			message = self.updates.recv()
			(filter, encdata) = message.split()
			data = self._decrypt(encdata)
			if filter == "update_listings":
				self.msg("Received listings update")
				self.server.listings = data["data"]
				self.server.seen = []
			elif filter == "update_whitelistings":
				self.msg("Received whitelistings update")
				self.server.whitelistings = data["data"]
				self.server.seen = []
			elif filter == "update_rules":
				self.msg("Received rules update")
				tmp_rules = {}
				for sensor in data["data"].keys():
					tmp_rules[sensor] = []
					for rule in data["data"][sensor]:
						tmp_rules[sensor].append([
							re.compile(rule[0]),
							rule[1],
							rule[2],
						])
				self.server.rules = tmp_rules
				self.server.seen = []

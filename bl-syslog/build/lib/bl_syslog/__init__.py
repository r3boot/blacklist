from Queue		import Queue
from datetime	import datetime
from socket		import socket, AF_INET, SOCK_DGRAM
from os			import fork, seteuid, setegid, geteuid, getegid, uname
from pwd		import getpwnam
from sys		import argv, exc_info, exit, modules
from threading	import Thread
from time		import sleep

import select
import re

from bl_syslog.api		import API
from bl_syslog.rfc3164	import *

class Server(Thread):
	listen_ip = None
	listen_port = None
	buffer_size = 1024
	errmsg = None
	stop = False

	def __init__(self, config):
		Thread.__init__(self)
		self.config = config
		self.api = API(config, self)
		self.queue = Queue()
		self.dispatcher = Dispatcher(self)
		self.year = datetime.strftime(datetime.now(), "%Y")
		self.stop = False

		self.sock = self.open_socket()
		if not self.sock:
			self.msg("Failed to initialize socket")
			exit(1)

		self.seen = []
		self.listings = self.fetch_listings()
		self.whitelistings = self.fetch_whitelistings()
		self.rules = self.fetch_rules()

		self.api.start()
		self.dispatcher.start()
		self.start()

	def msg(self, msg):
		print "[Server]: %s" % (msg)

	def open_socket(self):
		sock = None
		if not self.config["listen_ip"] or not self.config["listen_port"]:
			return None
		try:
			sock = socket(AF_INET, SOCK_DGRAM)
			sock.bind((self.config["listen_ip"], int(self.config["listen_port"])))
			self.msg("Listening on %s:%s" % (
				self.config["listen_ip"],
				self.config["listen_port"]
			))
		except:
			self.msg("Socket error: %s" % (exc_info()[1]))
			exit(1)
		return sock

	def fetch_listings(self):
		(result, listings) = self.api.get_listings()
		if not result:
			self.msg("Failed to retrieve listings")
			exit(1)
		else:
			self.msg("Fetched %s listings from broker" % (len(listings)))
		return listings

	def fetch_whitelistings(self):
		(result, listings) = self.api.get_whitelistings()
		if not result:
			self.msg("Failed to retrieve whitelistings")
			exit(1)
		else:
			self.msg("Fetched %s whitelistings from broker" % (len(listings)))
		return listings
		
	def fetch_rules(self):
		new_rules = {}
		(result, rules) = self.api.get_rules()
		if not result:
			self.msg("Failed to retrieve rules")
			exit(1)
		else:
			tot_rules = 0
			for sensor in rules.keys():
				new_rules[sensor] = []
				for rule in rules[sensor]:
					new_rules[sensor].append([
						re.compile(rule[0]),
						rule[1],
						rule[2],
					])
					tot_rules += 1
			self.msg("Fetched %s rules from broker" % (tot_rules))
		return new_rules

	def run(self):
		self.msg("Entering mainloop")
		try:
			os = uname()[0]
			if os in ["FreeBSD", "OpenBSD"]:
				kqueue = select.kqueue.fromfd(self.sock.fileno())
			elif os in ["Linux"]:
				epoll = select.epoll.fromfd(self.sock.fileno())
			while not self.stop:
				if os in ["FreeBSD", "OpenBSD"]:
					select.kevent(kqueue)
				elif os in ["Linux"]:
					epoll.poll()
				else:
					select(self.sock, [], [])
				try:
					data = self.sock.recv(self.buffer_size)
					msg = parse_message(data, self.year)
					self.queue.put(msg)
				except: pass
		except KeyboardInterrupt:
			self.stop = True
			self.msg("Exiting")

class Dispatcher(Thread):
	def __init__(self, server):
		Thread.__init__(self)
		self.setDaemon(True)
		self.server = server

	def msg(self, msg):
		print "[Dispatcher]: %s "% (msg)

	def af(self, dq):
		if ":" in dq: return 6
		elif "." in dq: return 4
		else: return -1

	def dqtoi(self, dq):
		# hex notation
		if dq.startswith("0x"):
			return long(dq[2:], 16)

		af = self.af(dq)
		if af == 4:
			q = dq.split('.')
			q.reverse()
			if len(q) > 4:
				raise ValueError, "%r: IPv4 address invalid: more than 4 bytes" % dq
			for x in q:
				if 0 > int(x) > 255:
					raise ValueError, "%r: IPv4 address invalid: bytes should be between 0 and 255" % dq
			while len(q) < 4:
				q.insert(1, '0')
			return sum(long(byte) << 8 * index for index, byte in enumerate(q))
		elif af == 6:
			hx = dq.split(':') # split hextets
			if ':::' in dq:
				raise ValueError, "%r: IPv6 address can't contain :::" % dq
			# Mixed address (or 4-in-6), ::ffff:192.0.2.42
			if '.' in dq:
				return self.dqtoi(hx[-1])
			if len(hx) > 8:
				raise ValueError, "%r: IPv6 address with more than 8 hexletts" % dq
			elif len(hx) < 8:
				if not '' in hx:
					raise ValueError, "%r: IPv6 address invalid: compressed format malformed" % dq
				elif not (dq.startswith('::') or dq.endswith('::')) and len([x for x in hx if x == '']) > 1:
					raise ValueError, "%r: IPv6 address invalid: compressed format malformed" % dq
				ix = hx.index('')
				px = len(hx[ix+1:])
				for x in xrange(ix+px+1, 8):
					hx.insert(ix, '0')
			elif dq.endswith('::'):
				pass
			elif '' in hx:
				raise ValueError, "%r: IPv6 address invalid: compressed format detected in full notation" % dq
			ip = ''
			hx = [x == '' and '0' or x for x in hx]
			for h in hx:
				if len(h) < 4:
					h = '%04x' % int(h, 16)
				if 0 > int(h, 16) > 0xffff:
					raise ValueError, "%r: IPv6 address invalid: hextets should be between 0x0000 and 0xffff" % dq
				ip += h
			return long(ip, 16)
		elif len(dq) == 32:
			# Assume full heximal notation
			return long(ip, 16)

		raise ValueError, "Invalid address input"

	def run(self):
		while not self.server.stop:
			if not self.server.queue.empty():
				msg = self.server.queue.get()
				is_listed = False
				is_whitelisted = False
				if msg["program"] in self.server.rules.keys():
					for rule in self.server.rules[msg["program"]]:
						match = rule[0].search(msg["message"])
						if match:
							dq = match.group(rule[1])
							ip = self.dqtoi(dq)
							reason = match.group(rule[2])
							if ip in self.server.seen:
								self.msg("%s has already been parsed, skipping" % (dq))
								break
							for entry in self.server.whitelistings:
								if ip >= entry[0] and ip <= entry[1]:
									self.msg("%s is whitelisted" % (dq))
									is_whitelisted = True
									self.server.seen.append(ip)
									break
							if not is_whitelisted:
								for entry in self.server.listings:
									if ip >= entry[0] and ip <= entry[1]:
										self.msg("%s is already listed" % (dq))
										is_listed = True
										self.server.seen.append(ip)
										break
							if not is_listed and not is_whitelisted:
								(result, listing) = self.server.api.add(
									match.group(rule[1]),
									match.group(rule[2]),
									msg["program"],
									msg["host"]
								)
								if result:
									print "%s: Added to blacklist" % (dq)
									self.server.seen.append(ip)
								else:
									print "%s: %s" % (dq, listing)
			else:
				sleep(0.1)

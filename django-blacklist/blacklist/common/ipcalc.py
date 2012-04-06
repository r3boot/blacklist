"""
This code uses pieces from Wijnand Modderman's excellent ipcalc.py
"""

class IPCalc:
	_bitmask = {
		'0': '0000', '1': '0001', '2': '0010', '3': '0011',
		'4': '0100', '5': '0101', '6': '0110', '7': '0111',
		'8': '1000', '9': '1001', 'a': '1010', 'b': '1011',
		'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'
	}

	iptobit = {
		4294967295: 0, 2147483648: 1, 1073741824: 2, 536870912: 3,
		268435456: 4, 134217728: 5, 67108864: 6, 33554432: 7,
		16777216: 8, 8388608: 9, 4194304: 10, 2097152: 11, 1048576: 12,
		524288: 13, 262144: 14, 131072: 15, 65536: 16, 32768: 17,
		16384: 18, 8192: 19, 4096: 20, 2048: 21, 1024: 22, 512: 23, 256: 24,
		128: 25, 64: 26, 32: 27, 16: 28, 8: 29, 4: 30, 2: 31, 1: 32
	}

	bittoip = {
		0:  4294967295, 1:  2147483648, 2: 1073741824, 3: 536870912,
		4:  268435456,  5:  134217728,  6: 67108864,   7: 33554432,
		8:  16777216,   9:  8388608,    10: 4194304,   11: 2097152,
		12: 1048576,    13: 524288,     14: 262144,    15: 131072,
		16: 65536,      17: 32768,      18: 16384,     19: 8192,
		20: 4096,       21: 2048,       22: 1024,      23: 512,
		24: 256,        25: 128,        26: 64,        27: 32,
		28: 16,         29: 8,          30: 4,         31: 2,
		32: 1
	}

	bittoint = {
		0:  0,          1:  2147483648, 2:  3221225472, 3:  3758096384,
		4:  4026531840, 5:  4160749568, 6:  4227858432, 7:  4261412864,
		8:  4278190080, 9:  4286578688, 10: 4290772992, 11: 4292870144,
		12: 4293918720, 13: 4294443008, 14: 4294705152, 15: 4294836224,
		16: 4294901760, 17: 4294934528, 18: 4294950912, 19: 4294959104,
		20: 4294963200, 21: 4294965248, 22: 4294966272, 23: 4294966784,
		24: 4294967040, 25: 4294967168, 26: 4294967232, 27: 4294967264,
		28: 4294967280, 29: 4294967288, 30: 4294967292, 31: 4294967294,
		32: 4294967295
	}

	def __init__(self):
		self.sizes = self.iptobit.keys()
		self.sizes.sort()
		self.sizes.reverse()

	def af(self, dq):
		""" Parse the dotted-quad and determine the address family

		expects: string containing dotted-quad (1.2.3.4)
		returns: integer containing address family (4, 6) or -1 for a failure
		"""
		if ":" in dq: return 6
		elif "." in dq: return 4
		else: return -1

	def ctodq(self, c):
		""" Convert a CIDR address to a dotted-quad with bitmask

		expects: string containing a CIDR address (1.2.3.4/5)
		returns: tuple containing the dotted-quad and the netmask
		"""
		if "/" in c:
			(dq, mask) = c.split("/")
			mask = int(mask)
		else:
			dq = c
			if self.af(dq) == 4:
				mask = 32
			else:
				mask = 128
		return (dq, mask)

	def dqtoi(self, dq):
		""" Convert a (hexadecimal) dotted-quad into an integer

		expects: string containing dotted-quad. This can be in hex if prefixed with '0x'
		returns: integer containing ip address
		"""
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

	def itodq(self, n, v):
		""" Convert an integer to a dotted-quad

		expects: integer containing ip address
		expects: integer containing address family (4, 6)
		returns: string containing dotted-quad
		"""
		if v == 4:
			return '.'.join(map(str, [(n>>24) & 0xff, (n>>16) & 0xff, (n>>8) & 0xff, n & 0xff]))
		elif v ==6:
			n = '%032x' % n
			hextets = []
			for x in range(0, 32, 4):
				hextets.append('%x' % int(n[x:x+4], 16))
			return ':'.join(self.compress6(hextets))
		raise ValueError, "Invalid address input"

	def dqtob(self, dq):
		""" Convert dotted-quad to binary

		expects: string containing dotted quad
		returns: string containing ip address in binary
		"""
		h = hex(self.dqtoi(dq)).lower().rstrip('l')
		b = ''.join(self._bitmask[x] for x in h[2:])
		l = self.af(dq) == 4 and 32 or 128
		return ''.join('0' for x in xrange(len(b), l)) + b

	def dqtoh(self, dq):
		""" Convert a dotted-quad to hexadecimal

		expects: string containing dotted-quad
		returns: string containing ip address in hexadecimal
		"""
		af = self.af(dq)
		if af == 4: return '%08x' % self.dqtoi(dq)
		else: return '%032x' % self.dqtoi(dq)

	def netmask(self, c):
		""" Extract the netmask from a given CIDR address

		expects: string containing CIDR address (1.2.3.4/5)
		returns: string containing the netmask
		"""
		(dq, mask) = self.ctodq(c)
		af = self.af(dq)
		if af == 4:
			return self.itodq(0xffffffffL >> (32-mask) << (32-mask), af)
		else:
			return self.itodq(0xffffffffffffffffffffffffffffffffL >> (128-mask) << (128-mask), af)

	def first(self, c):
		""" Given a CIDR address, return the first ip in this subnet

		expects: string containing CIDR address
		returns: string containing first address from this subnet
		"""
		(dq, cidrmask) = self.ctodq(c)
		i = self.dqtoi(dq)
		af = self.af(dq)
		mask = self.dqtoi(self.netmask(c))
		return self.itodq(i & mask, af)

	def last(self, c):
		""" Given a CIDR address, return the last ip in this subnet

		expects: string containing CIDR address
		returns: string containing last address from this subnet
		"""
		af = self.af(self.ctodq(c)[0])
		first = self.dqtoi(self.first(c))
		mask = self.dqtoi(self.netmask(c))
		if af == 4:
			return self.itodq(first | (0xffffffff - mask), af)
		else:
			return self.itodq(first | (0xffffffffffffffffffffffffffffffffL - mask), af)

	def size(self, c):
		""" Given a CIDR address, return the total amount of ip's in this subnet

		expects: string containing CIDR address
		returns: integer containing the amount of ip's in this subnet
		"""
		(dq, cidrmask) = self.ctodq(c)
		af = self.af(dq)
		i = self.dqtoi(dq)
		mask = self.dqtoi(self.netmask(c))
		return max(0, 2 ** (af == 4 and 32 or 128) - mask)

	def in_network(self, other, net):
		""" Given a CIDR address, find out if this address is part of a network

		expects: string containing CIDR address (other; the needle)
		expects: string containing CIDR address (net; the haystack)
		returns: boolean which is true if other is part of net
		"""
		(dq, cidrmask) = self.ctodq(net)
		i = self.dqtoi(dq)
		size = self.size(net)
		(dq_other, cidrmask) = self.ctodq(other)
		i_other = self.dqtoi(dq_other)
		size_other = self.size(other)
		return i_other >= i and i_other < i + size - size_other + 1

	def parent(self, net, networks):
		""" Given a network and a list of all networks, find out to which supernet a network belongs to

		expects: string containing CIDR network (net)
		expects: list of strings containing all CIDR networks we want to search (networks)
		returns: string containing the CIDR supernet that net belongs to
		"""
		(dq, cidrmask) = self.ctodq(net)
		potential = []
		for n in networks:
			(dq, cidrmask_n) = self.ctodq(n)
			if self.in_network(net, n):
				potential.append(n)
		p = None
		for n in potential:
			if not p:
				p = n
				continue
			(dq, cidrmask_n) = self.ctodq(n)
			(dq, cidrmask_p) = self.ctodq(p)
			if cidrmask_n > cidrmask_p and cidrmask_n != 0 and n != net:
				p = n
		return p

	def compress6(self, hextets):
		""" Compress an IPv6 address

		expects: string containing an IPv6 address
		returns: string containing the compressed IPv6 address

		Taken from http://ipaddr-py.googlecode.com/svn/trunk/ipaddr.py
		"""
		best_doublecolon_start = -1
		best_doublecolon_len = 0
		doublecolon_start = -1
		doublecolon_len = 0
		for index in range(len(hextets)):
			if hextets[index] == '0':
				doublecolon_len += 1
				if doublecolon_start == -1:
					doublecolon_start = index
				if doublecolon_len > best_doublecolon_len:
					best_doublecolon_len = doublecolon_len
					best_doublecolon_start = doublecolon_start
			else:
				doublecolon_len = 0
				doublecolon_start = -1

		if best_doublecolon_len > 1:
			best_doublecolon_end = (best_doublecolon_start + best_doublecolon_len)
			if best_doublecolon_end == len(hextets):
				hextets += ['']
			hextets[best_doublecolon_start:best_doublecolon_end] = ['']
			if best_doublecolon_start == 0:
				hextets = [''] + hextets
		return hextets

	def parse_addr(self, addr):
		if "/" in addr:
			(ip, mask) = addr.split('/')
		else:
			af = self.af(addr)
			ip = addr
			if af == 4:
				mask = 32
			elif af == 6:
				mask = 128
		return (ip, mask)

	def aggregates(self, ip, num_ips, subnets):
		"""
		Given a starting ip and the total number of ip's, calculate
		the least-specific subnets covering the complete set of ip's
		"""
		for k in self.sizes:
			if k <= num_ips and (ip & self.bittoint[self.iptobit[k]]) == ip:
				subnets.append([ip, self.iptobit[k]]) 
				num_ips = num_ips - k
				ip += k
				break
		if num_ips > 0:
			subnets = self.aggregates(ip, num_ips, subnets)
		return subnets

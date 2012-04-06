from datetime	import datetime
from socket	import gethostname, socket, AF_INET, SOCK_DGRAM
from os		import fork, seteuid, setegid, geteuid, getegid
from pwd	import getpwnam
from sys	import argv, exc_info, exit

'''
rfc3164.py

Various functions for working with RFC3164 data
'''

facilities = {
	0:	"kern",
	1:	"user",
	2:	"mail",
	3:	"system",
	4:	"auth",
	5:	"syslog",
	6:	"lpr",
	7:	"news",
	8:	"uucp",
	9:	"cron",
	10:	"authpriv",
	11:	"ftp",
	16:	"local0",
	17:	"local1",
	18:	"local2",
	19:	"local3",
	20:	"local4",
	21:	"local5",
	22:	"local6",
	23:	"local7",
}

priorities = {
	0:	"emerg",	# LOG_EMERG
	1:	"alert",	# LOG_ALERT
	2:	"crit",		# LOG_CRIT
	3:	"error",	# LOG_ERR
	4:	"warn",		# LOG_WARNING
	5:	"notice",	# LOG_NOTICE
	6:	"info",		# LOG_INFO
	7:	"debug",	# LOG_DEBUG
}

def parse_pri_header(header):
	'''
	parse_pri_header(header) -> (facility, priority)

	Returns the facility and priority for a given PRI header. See
	include/syslog.h and RFC3164 for details
	'''
	header = int(header)
	facility = facilities[((header & 0x3f8) >> 3)]
	priority = priorities[(header & 0x07)]
	return (facility, priority)

def parse_message(data, year):
	'''
	parse_message() -> dict(syslog message)

	Parse a single line of syslog data into a dictionary
	'''
	msg = {}

	pri = data.split(">")[0]
	pri = int(pri.replace("<", ""))
	(msg["facility"], msg["priority"]) = parse_pri_header(pri)

	t = data.split()
	t[0] = t[0].split(">")[1]
	msg["ts"] = datetime.strptime("%s %s %s %s" % (year, t[0], t[1], t[2]), "%Y %b %d %H:%M:%S")
	msg["host"] = t[3]
	if "[" in t[4]:
		msg["program"] = t[4].split("[")[0]
	else:
		msg["program"] = t[4].split(":")[0]
	msg["message"] = " ".join(t[5:])

	return msg

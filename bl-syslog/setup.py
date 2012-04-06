#!/usr/bin/env python

from distutils.core	import setup

setup(
	name="bl-syslog",
	version="0.4",
	description="Blacklist syslog daemon",
	author="r3boot",
	author_email="r3boot@r3blog.nl",
	url="https://r3blog.nl",
	packages=[
		"bl_syslog",
	],
	scripts=[
		"bin/bl-syslog",
	],
	data_files=[
		("/etc",	["conf/bl-syslog.conf"]),
	]
)

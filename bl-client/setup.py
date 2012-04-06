#!/usr/bin/env python

from distutils.core	import setup

setup(
	name="bl-client",
	version="0.4",
	description="Blacklist client",
	author="r3boot",
	author_email="r3boot@r3blog.nl",
	url="https://r3blog.nl",
	scripts=[
		"bin/bl-client",
	],
	data_files=[
		("/etc",	["conf/bl-client.conf"]),
	]
)

#!/usr/bin/env python

from distutils.core	import setup

setup(
	name="bl-broker",
	version="0.4",
	description="Blacklist broker daemon",
	author="r3boot",
	author_email="r3boot@r3blog.nl",
	url="https://r3blog.nl",
	scripts=[
		"bin/bl-broker",
	],
	data_files=[
		("/etc",	["conf/bl-broker.conf"]),
	]
)

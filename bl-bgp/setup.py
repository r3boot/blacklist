#!/usr/bin/env python

from distutils.core	import setup

setup(
	name="bl-bgp",
	version="0.4",
	description="Blacklist BGP configuration daemon",
	author="r3boot",
	author_email="r3boot@r3blog.nl",
	url="https://r3blog.nl",
	scripts=[
		"bin/bl-bgp",
	],
	data_files=[
		("/etc",	["conf/bl-bgp.conf"]),
		("/usr/local/share/bl-bgp",	[
				"templates/bird.conf.template",
				"templates/bird6.conf.template",
		]),
	]
)

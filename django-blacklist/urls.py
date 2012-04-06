from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r"^$",				"overview.views.index"),
	(r"^login/$",		"users.views.login_form"),
	(r"^logout/$",		"users.views.logout_form"),
	(r"^listing/",		include("blacklist.urls.listing")),
	(r"^registry/",		include("blacklist.urls.registry")),
	(r"^whitelist/",	include("blacklist.urls.whitelist")),
	(r"^peering/",		include("blacklist.urls.peering")),
	(r"^rule/",			include("blacklist.urls.rule")),
)

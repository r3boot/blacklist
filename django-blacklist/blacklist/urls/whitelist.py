from django.conf.urls.defaults	import *

urlpatterns = patterns(
	"blacklist.views.whitelisting",
	(r"^$",		"whitelistings"),
	(r"^add/$",	"add"),
)

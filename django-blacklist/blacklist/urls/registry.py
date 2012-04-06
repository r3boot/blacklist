from django.conf.urls.defaults	import *

urlpatterns = patterns(
	"blacklist.views.registry",
	(r"country/$",		"countries"),
	(r"rir/$",			"rirs"),
	(r"provider/$",		"providers"),
	(r"subnet/$",		"subnets"),
)

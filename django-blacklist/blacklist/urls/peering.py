from django.conf.urls.defaults	import *

urlpatterns = patterns(
	"blacklist.views.peering",
	(r"^$",		"peerings"),
	(r"^add/$",	"add"),
)

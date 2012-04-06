from django.conf.urls.defaults	import *

urlpatterns = patterns(
	"blacklist.views.listing",
	(r"^$",		"listings"),
	(r"^add/$",	"add"),
)

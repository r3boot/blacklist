from django.conf.urls.defaults	import *

urlpatterns = patterns(
	"blacklist.views.rule",
	(r"^$",		"rules"),
	(r"^add/$",	"add"),
)

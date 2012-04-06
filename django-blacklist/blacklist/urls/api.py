from django.conf.urls.defaults	import *

urlpatterns = patterns(
	"blacklist.views.api",
	(r"^(?P<data>[a-zA-Z0-9-_=]+)$",		"dispatch"),
)

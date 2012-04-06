from django.contrib.auth.decorators	import login_required
from django.shortcuts			import render_to_response
from django.template			import RequestContext

def index(request):
	errmsg = ""
	return render_to_response("overview/index.html", {
		"errmsg":		errmsg,
	}, context_instance=RequestContext(request))

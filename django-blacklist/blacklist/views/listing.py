from django.contrib.auth.decorators	import login_required
from django.core.paginator			import Paginator,InvalidPage,EmptyPage
from django.core.urlresolvers		import reverse
from django.http					import HttpResponse,HttpResponseRedirect
from django.shortcuts				import render_to_response
from django.template				import RequestContext

from blacklist.common.broker		import Broker
from blacklist.common.ipcalc		import IPCalc
from blacklist.common.search		import Search
from blacklist.middleware.listing	import Listing
from blacklist.table.listing		import ListingTable
from blacklist.forms.listing		import ListingForm
from blacklist.forms.search			import SearchForm

import socket

listing = Listing()
ipcalc = IPCalc()
broker = Broker()

@login_required
def listings(request):
	errmsg = ""

	if "q" in request.GET.keys() and len(request.GET["q"]) != 0:
		s = Search(
			model=Listing(),
			fields={
				"ip":			"ip__ip",
				"reason":		"reason__reason",
				"sensor":		"sensor__name",
				"sensor_host":	"sensor_host__hostname",
				"timestamp":	"timestamp",
				"duration":		"duration__duration",
				"reporter":		"reporter",
			}
		)
		(result, listing_data) = s.find(request.GET["q"])
		if not result:
			errmsg = listing_data,
			(result, listing_data) = listing.all()
	else:
		(result, listing_data) = listing.all()
		if not result: return HttpResponseRedirect("/")

	try: page = int(request.GET.get('page', '1'))
	except: page = 1

	listing_table = ListingTable(
		listing_data,
		order_by=request.GET.get('sort', 'title')
	)

	if request.method == "GET":
		search_form = SearchForm(request.GET)
	else:
		search_form = SearchForm()

	return render_to_response("listing/overview.html", {
		"errmsg":			errmsg,
		"search_form":		search_form,
		"listing_table":	listing_table,
	}, context_instance=RequestContext(request))

@login_required
def add(request):
	errmsg = ""

	if request.method == "POST":
		form = ListingForm(request.POST)
		if form.is_valid():
			ip = form.cleaned_data["ip"]
			reason = form.cleaned_data["reason"]
			try:
				ipcalc.dqtoi(ip)
			except:
				errmsg = "%s is nto a valid ip address"
			finally:
				(result, entry) = listing.add(
					ip=ip,
					reason=reason,
					sensor="webinterface",
					sensor_host=socket.gethostname().split(".")[0],
					reporter=str(request.user),
				)
				if result:
					broker.update_listings()
					return HttpResponseRedirect(reverse("blacklist.views.listing.listings"))
				else:
					errmsg = entry
	else:
		form = ListingForm()

	return render_to_response("listing/add.html", {
		"errmsg":	errmsg,
		"form":		form,
	}, context_instance=RequestContext(request))

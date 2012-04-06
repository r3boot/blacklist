from django.contrib.auth.decorators	import login_required
from django.core.paginator			import Paginator,InvalidPage,EmptyPage
from django.core.urlresolvers		import reverse
from django.http					import HttpResponse,HttpResponseRedirect
from django.shortcuts				import render_to_response
from django.template				import RequestContext

from blacklist.common.config			import Config
from blacklist.common.ipcalc			import IPCalc
from blacklist.common.broker			import Broker
from blacklist.common.search			import Search
from blacklist.middleware.whitelisting	import WhiteListing
from blacklist.table.whitelisting		import WhiteListingTable
from blacklist.forms.whitelisting		import WhiteListingForm
from blacklist.forms.search				import SearchForm

config = Config()
whitelisting = WhiteListing()
ipcalc = IPCalc()
broker = Broker()

@login_required
def whitelistings(request):
	errmsg = ""

	if "q" in request.GET.keys() and len(request.GET["q"]) != 0:
		s = Search(
			model=WhiteListing(),
			fields={
				"ip":		"ip__ip",
				"hostname":	"hostname",
			}
		)
		(result, whitelist_data) = s.find(request.GET["q"])
		if not result:
			errmsg = whitelist_data
			(result, whitelist_data) = whitelisting.all()
	else:
		(result, whitelist_data) = whitelisting.all()
		if not result: return HttpResponseRedirect("/")

	try: page = int(request.GET.get('page', '1'))
	except: page = 1

	whitelist_table = WhiteListingTable(
		whitelist_data,
		order_by=request.GET.get('sort', 'title')
	)

	if request.method == "GET":
		search_form = SearchForm(request.GET)
	else:
		search_form = SearchForm()

	return render_to_response("whitelist/overview.html", {
		"errmsg":			errmsg,
		"search_form":		search_form,
		"whitelist_table":	whitelist_table,
	}, context_instance=RequestContext(request))

@login_required
def add(request):
	errmsg = ""
	if request.method == "POST":
		form = WhiteListingForm(request.POST)
		if form.is_valid():
			ip = form.cleaned_data["ip"]
			hostname = form.cleaned_data["hostname"]
			try:
				if "/" in ip:
					(dq, mask) = ipcalc.parse_addr(ip)
				else:
					dq = ip
				ipcalc.dqtoi(dq)
			except:
				errmsg = "%s is not a valid ip address" % (ip)

			if errmsg == "":
				(result, entry) = whitelisting.add(
					ip=ip,
					hostname=hostname,
				)
				if result:
					broker.update_whitelistings()
					return HttpResponseRedirect(reverse("blacklist.views.whitelisting.whitelistings"))
				else:
					errmsg = entry
	else:
		form = WhiteListingForm()

	return render_to_response("whitelist/add.html", {
		"errmsg":	errmsg,
		"form":		form,
	}, context_instance=RequestContext(request))

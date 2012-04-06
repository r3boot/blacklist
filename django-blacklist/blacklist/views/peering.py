from django.contrib.auth.decorators	import login_required
from django.core.paginator			import Paginator,InvalidPage,EmptyPage
from django.core.urlresolvers		import reverse
from django.http					import HttpResponse,HttpResponseRedirect
from django.shortcuts				import render_to_response
from django.template				import RequestContext

from blacklist.common.broker		import Broker
from blacklist.common.ipcalc		import IPCalc
from blacklist.middleware.peering	import Peering
from blacklist.middleware.ip		import IP
from blacklist.middleware.host		import Host
from blacklist.middleware.asnum		import ASNum
from blacklist.middleware.key		import Key
from blacklist.table.peering		import PeeringTable
from blacklist.forms.peering		import PeeringForm

broker = Broker()
ipcalc = IPCalc()
peering = Peering()
ip = IP()
host = Host()
asnum = ASNum()
key = Key()

@login_required
def peerings(request):
	(result, peering_data) = peering.all()
	if not result: return HttpResponseRedirect("/")

	try: page = int(request.GET.get('page', '1'))
	except: page = 1

	peering_table = PeeringTable(
		peering_data,
		order_by=request.GET.get('sort', 'title')
	)

	return render_to_response("peering/overview.html", {
		"peering_table":	peering_table,
	}, context_instance=RequestContext(request))

@login_required
def add(request):
	errmsg = ""

	if request.method == "POST":
		form = PeeringForm(request.POST)
		if form.is_valid():
			hostname = form.cleaned_data["hostname"]
			peer_ip = form.cleaned_data["ip"]
			peer_asnum = form.cleaned_data["asnum"]
			peer_key = form.cleaned_data["key"]

			## TODO: Fix proper RIR detection
			(result, entry_asnum) = asnum.get(asnum=peer_asnum)
			if not result:
				(result, entry_asnum) = asnum.add(asnum=peer_asnum, rir="Unknown")
				if not result:
					errmsg = "Failed to add ASNum"

			(result, entry_host) = host.get(hostname=hostname)
			if not result:
				(result, entry_host) = host.add(
					hostname=hostname,
					ip=peer_ip,
					user=request.user,
				)
				if not result:
					errmsg = "Failed to add Host"

			(result, entry_key) = key.get(name="%s-BGP" % (hostname))
			if not result:
				(result, entry_key) = key.add(
					name="%s-BGP" % (hostname),
					data=peer_key,
				)
				if not result:
					errmsg = "Failed to add Key"

			(result, entry) = peering.get(peer=entry_host)
			if not result:
				(result, entry) = peering.add(
					peer=entry_host,
					asnum=entry_asnum,
					user=request.user,
					key=entry_key
				)
			if result:
				# broker.update_peerings()
				return HttpResponseRedirect(reverse("blacklist.views.peering.peerings"))
			else:
				errmsg = entry
	else:
		form = PeeringForm()

	return render_to_response("peering/add.html", {
		"errmsg":	errmsg,
		"form":		form,
	}, context_instance=RequestContext(request))

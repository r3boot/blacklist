from django.contrib.auth.decorators	import login_required
from django.core.paginator		import Paginator,InvalidPage,EmptyPage
from django.http			import HttpResponse,HttpResponseRedirect
from django.shortcuts			import render_to_response
from django.template			import RequestContext

from blacklist.common.config		import Config
from blacklist.common.search		import Search
from blacklist.common.broker		import Broker
from blacklist.forms.search			import SearchForm
from blacklist.middleware.country	import Country
from blacklist.middleware.rir		import RIR
from blacklist.middleware.asnum		import ASNum
from blacklist.middleware.subnet	import Subnet 
from blacklist.table.country		import CountryTable
from blacklist.table.rir			import RIRTable
from blacklist.table.asnum			import ASNumTable
from blacklist.table.subnet			import SubnetTable

cfg = Config()
country = Country()
rir = RIR()
asnum = ASNum()
subnet = Subnet()
broker = Broker()

@login_required
def countries(request):
	errmsg = ""
	listing_changed = False
	whitelisting_changed = False

	for item in request.GET.keys():
		if item.startswith("id_"):
			(result, cc) = country.get(id=item[3:])
			if result:
				if request.GET["bulk_action"] == "blacklist":
					cc.listed = not cc.listed
					listing_changed = True
					if cc.whitelisted:
						cc.whitelisted = False
						whitelisting_changed = True
				elif request.GET["bulk_action"] == "whitelist":
					cc.whitelisted = not cc.whitelisted
					whitelisting_changed = True
					if cc.listed:
						cc.listed = False
						listing_changed = True
				cc.save()

	if listing_changed:
		broker.update_listings()
	if whitelisting_changed:
		broker.update_whitelistings()

	if "q" in request.GET.keys() and len(request.GET["q"]) != 0:
		s = Search(
			model=Country(),
			fields={
				"code":			"code",
				"name":			"name",
				"additional":	"additional",
				"rir":			"rir__name",
				"listed":		"listed",
				"whitelisted":	"whitelisted",
			}
		)
		(result, country_data) = s.find(request.GET["q"])
		if not result:
			errmsg = country_data
			(result, country_data) = country.all()
	else:
		(result, country_data) = country.all()
		if not result: return HttpResponseRedirect("/")

	try: page = int(request.GET.get('page', '1'))
	except: page = 1

	country_table = CountryTable(
		country_data,
		order_by=request.GET.get('sort', 'title')
	)

	if request.method == "GET":
		search_form = SearchForm(request.GET)
	else:
		search_form = SearchForm()

	return render_to_response("registry/country/overview.html", {
		"errmsg":			errmsg,
		"country_table":	country_table,
		"search_form":		search_form,
	}, context_instance=RequestContext(request))

@login_required
def rirs(request):
	listing_changed = False
	whitelisting_changed = False

	for item in request.GET.keys():
		if item.startswith("id_"):
			(result, r) = rir.get(id=item[3:])
			if result:
				if request.GET["bulk_action"] == "blacklist":
					r.listed = not r.listed
					listing_changed = True
					if r.whitelisted:
						r.whitelisted = False
						whitelisting_changed = False
				elif request.GET["bulk_action"] == "whitelist":
					r.whitelisted = not r.whitelisted
					whitelisting_changed = True
					if r.listed:
						r.listed = False
						listing_changed = True
				r.save()

	if listing_changed:
		broker.update_listings()
	if whitelisting_changed:
		broker.update_whitelistings()
		
	(result, rir_data) = rir.all()
	if not result: return HttpResponseRedirect("/")

	try: page = int(request.GET.get('page', '1'))
	except: page = 1

	rir_table = RIRTable(
		rir_data,
		order_by=request.GET.get('sort', 'title')
	)

	return render_to_response("registry/rir/overview.html", {
		"rir_table":	rir_table,
	}, context_instance=RequestContext(request))

@login_required
def providers(request):
	errmsg = ""
	listing_changed = False
	whitelisting_changed = False

	for item in request.GET.keys():
		if item.startswith("id_"):
			(result, asn) = asnum.get(id=item[3:])
			if result:
				if request.GET["bulk_action"] == "blacklist":
					asn.listed = not asn.listed
					listing_changed = True
					if asn.whitelisted:
						whitelisting_changed = True
						asn.whitelisted = False
				elif request.GET["bulk_action"] == "whitelist":
					asn.whitelisted = not asn.whitelisted
					whitelisting_changed = True
					if asn.listed:
						listing_changed = True
						asn.listed = False
				asn.save()

	if listing_changed:
		broker.update_listings()
	if whitelisting_changed:
		broker.update_whitelistings()

	if "q" in request.GET.keys() and len(request.GET["q"]) != 0:
		s = Search(
			model=ASNum(),
			fields={
				"asnum":	"asnum",
				"name":		"name",
				"country":	"country__name",
				"code":		"country__code",
				"rir":		"rir__name",
				"regdate":	"regdate",
				"listed":		"listed",
				"whitelisted":	"whitelisted",
			}
		)
		(result, asnum_data) = s.find(request.GET["q"])
		if not result:
			errmsg = asnum_data
			(result, asnum_data) = asnum.all()
	else:
		(result, asnum_data) = asnum.all()
		if not result: return HttpResponseRedirect("/")

	try: page = int(request.GET.get('page', '1'))
	except: page = 1

	asnum_table = ASNumTable(
		asnum_data,
		order_by=request.GET.get('sort', 'title')
	)

	if request.method == "GET":
		search_form = SearchForm(request.GET)
	else:
		search_form = SearchForm()

	return render_to_response("registry/provider/overview.html", {
		"errmsg":		errmsg,
		"asnum_table":	asnum_table,
		"search_form":	search_form,
	}, context_instance=RequestContext(request))

@login_required
def subnets(request):
	errmsg = ""
	listing_changed = False
	whitelisting_changed = False

	for item in request.GET.keys():
		if item.startswith("id_"):
			(result, sn) = subnet.get(id=item[3:])
			if result:
				if request.GET["bulk_action"] == "blacklist":
					sn.listed = not sn.listed
					listing_changed = True
					if sn.whitelisted:
						sn.whitelisted = False
						whitelisting_changed = True
				elif request.GET["bulk_action"] == "whitelist":
					sn.whitelisted = not sn.whitelisted
					whitelisting_changed = True
					if sn.listed:
						sn.listed = False
						listing_changed = True
				sn.save()

	if listing_changed:
		broker.update_listings()
	if whitelisting_changed:
		broker.update_whitelistings()

	if "q" in request.GET.keys() and len(request.GET["q"]) != 0:
		s = Search(
			model=Subnet(),
			fields={
				"subnet":		"subnet",
				"mask":			"mask",
				"last":			"last",
				"provider":		"asnum__name",
				"af":			"af",
				"code":			"country__code",
				"country":		"country__name",
				"rir":			"rir__name",
				"regdate":		"regdate",
				"listed":		"listed",
				"whitelisted":	"whitelisted",
			}
		)

		(result, subnet_data) = s.find(request.GET["q"])
		if not result:
			errmsg = subnet_data
			(result, subnet_data) = subnet.all()
	else:
		(result, subnet_data) = subnet.all()
		if not result: return HttpResponseRedirect("/")

	try: page = int(request.GET.get('page', '1'))
	except: page = 1

	subnet_table = SubnetTable(
		subnet_data,
		order_by=request.GET.get('sort', 'title')
	)

	if request.method == "GET":
		search_form = SearchForm(request.GET)
	else:
		search_form = SearchForm()

	return render_to_response("registry/subnet/overview.html", {
		"errmsg":		errmsg,
		"search_form":	search_form,
		"subnet_table":	subnet_table,
	}, context_instance=RequestContext(request))

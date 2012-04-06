from django.contrib.auth.decorators	import login_required
from django.core.paginator			import Paginator,InvalidPage,EmptyPage
from django.core.urlresolvers		import reverse
from django.http					import HttpResponse,HttpResponseRedirect
from django.shortcuts				import render_to_response
from django.template				import RequestContext

from blacklist.common.broker	import Broker
from blacklist.middleware.rule	import Rule
from blacklist.table.rule		import RuleTable
from blacklist.forms.rule		import RuleForm

broker = Broker()
rule = Rule()

@login_required
def rules(request):
	(result, rule_data) = rule.all()
	if not result: return HttpResponseRedirect("/")

	try: page = int(request.GET.get('page', '1'))
	except: page = 1

	rule_table = RuleTable(
		rule_data,
		order_by=request.GET.get('sort', 'title')
	)

	return render_to_response("rule/overview.html", {
		"rule_table":	rule_table,
	}, context_instance=RequestContext(request))

@login_required
def add(request):
	errmsg = ""

	if request.method == "POST":
		form = RuleForm(request.POST)
		if form.is_valid():
			r = form.cleaned_data["rule"]
			sensor = form.cleaned_data["sensor"]
			pos_ip = form.cleaned_data["pos_ip"]
			pos_reason = form.cleaned_data["pos_reason"]
			(result, entry) = rule.add(
				rule=r,
				sensor=sensor,
				pos_ip=pos_ip,
				pos_reason=pos_reason,
			)
			if result:
				broker.update_rules()
				return HttpResponseRedirect(reverse("blacklist.views.rule.rules"))
			else:
				errmsg = entry
	else:
		form = RuleForm()

	return render_to_response("rule/add.html", {
		"errmsg":	errmsg,
		"form":		form,
	}, context_instance=RequestContext(request))

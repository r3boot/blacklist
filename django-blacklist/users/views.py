from django.contrib.auth	import authenticate
from django.contrib.auth	import login
from django.contrib.auth	import logout
from django.http		import HttpResponse
from django.http		import HttpResponseRedirect
from django.template		import RequestContext
from django.shortcuts		import render_to_response
from django.utils.encoding	import smart_unicode

from users.forms	import LoginForm

def login_form(request):
	errmsg = ""
	try: prevpage = smart_unicode(request.GET["next"])
	except KeyError: prevpage = "/"
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(
				username=form.cleaned_data["username"],
				password=form.cleaned_data["password"],
			)
			if form.cleaned_data["prevpage"] == "login":
				prevpage = "/"
			else:
				prevpage = form.cleaned_data["prevpage"]
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(prevpage)
				else:
					errmsg = "User is disabled"
		else:
			errmsg = "Invalid username/password"
	else:
		form = LoginForm(initial=dict(prevpage=prevpage))

	return render_to_response("users/login.html", {
		"errmsg":	errmsg,
		"form":		form,
	}, context_instance=RequestContext(request))

def logout_form(request):
	logout(request)
	return HttpResponseRedirect("/")

def manager_form(request):
	return HttpResponseRedirect("/")		

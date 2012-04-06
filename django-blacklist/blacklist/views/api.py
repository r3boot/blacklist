from django.contrib.auth	import authenticate
from django.http			import HttpResponse,HttpResponseRedirect
from django.shortcuts		import render_to_response
from django.template		import RequestContext

from blacklist.common.api			import API
from blacklist.common.config		import Config
from blacklist.common.encryption	import Encryption

import datetime
import random
import time

config = Config()
api = API()
enc = Encryption(config["blacklist.api.psk"])

def dispatch(request, data):
	response = {
		"result":	False,
		"data":		None,
		"random":	random.random()*time.mktime(datetime.datetime.timetuple(datetime.datetime.now()))
	}

	try:
		data = enc.decrypt(data)
	except:
		response["data"] = "Failed to decrypt data"

	user = authenticate(username=data['username'], password=data['password'])
	if not user:
		response["data"] = "Failed to authenticate"

	if data.has_key('action'):
		if data['action'] == 'add':
			(response["result"], response["data"]) = api.add(data)
		elif data['action'] == 'get_rules':
			(response["result"], response["data"]) = api.get_rules()
		else:
			response["data"] = "Invalid action specified"
	else:
		response["data"] == "No action specified"

	return HttpResponse(enc.encrypt(response))

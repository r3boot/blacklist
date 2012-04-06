#!/usr/bin/env python

from cPickle	import dumps
from os		import environ
from sys	import path, argv, exit

path.append("/mnt/data/blacklist/django")
environ["DJANGO_SETTINGS_MODULE"] = "blacklist.settings"

from blacklist.db.models	import *

backup_dir = "/mnt/data/blacklist/django/blacklist/scripts/backup"

if __name__ == "__main__":
	if len(argv) != 2:
		print "Usage: %s <output file>" % (argv[0])
		exit(1)
	print "==> Gathering DB data"
	data = {}
	data["asnumregistry"] = ASNumRegistry.objects.all()
	data["blacklist"] = Blacklist.objects.all()
	data["countrycode"] = CountryCode.objects.all()
	data["history"] = History.objects.all()
	data["peering"] = Peering.objects.all()
	data["provider"] = Provider.objects.all()
	data["providersubnet"] = ProviderSubnet.objects.all()
	data["rir"] = RIR.objects.all()
	data["settingstore"] = SettingStore.objects.all()
	pickled_data = dumps(data)

	for i in data.keys():
		print "==> Saved %s %s objects" % (len(data[i]), i)

	print "==> Writing data to %s" % (argv[1])
	open(argv[1], "w").write(pickled_data)

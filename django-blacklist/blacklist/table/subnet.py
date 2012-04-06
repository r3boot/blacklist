
import django_tables	as tables
from blacklist.models	import Subnet

class SubnetTable(tables.ModelTable):
	id				= tables.Column(sortable=False, visible=False)
	subnet			= tables.Column()
	mask			= tables.Column(sortable=False, visible=False)
	af				= tables.Column(sortable=False, visible=False)
	asnum			= tables.Column(name="Provider", data="asnum__name")
	listed			= tables.Column()
	whitelisted		= tables.Column()

	class Meta:
		model	= Subnet
		exclude	= ["last", "num_listed", "num_whitelisted"]

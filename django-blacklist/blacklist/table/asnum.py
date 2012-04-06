
import django_tables	as tables
from blacklist.models	import ASNum

class ASNumTable(tables.ModelTable):
	id				= tables.Column(sortable=False, visible=False)
	asnum			= tables.Column()
	name			= tables.Column()
	whois_data		= tables.Column(sortable=False, visible=False)
	country			= tables.Column()
	listed			= tables.Column()
	whitelisted		= tables.Column()
	num_subnets		= tables.Column(sortable=False, visible=False)
	num_listed		= tables.Column(sortable=False, visible=False)
	num_whitelisted	= tables.Column(sortable=False, visible=False)
	num_history		= tables.Column(sortable=False, visible=False)

	class Meta:
		model	= ASNum

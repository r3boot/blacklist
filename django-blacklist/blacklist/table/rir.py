
import django_tables	as tables
from blacklist.models	import RIR

class RIRTable(tables.ModelTable):
	id		= tables.Column(sortable=False, visible=False)
	name		= tables.Column()
	whois		= tables.Column()
	listed		= tables.Column()
	whitelisted	= tables.Column()
	num_providers	= tables.Column(sortable=False, visible=False)
	num_subnets	= tables.Column(sortable=False, visible=False)
	num_listed	= tables.Column(sortable=False, visible=False)
	num_whitelisted	= tables.Column(sortable=False, visible=False)
	num_history	= tables.Column(sortable=False, visible=False)

	class Meta:
		model	= RIR

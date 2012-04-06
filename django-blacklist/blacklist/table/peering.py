
import django_tables	as tables
from blacklist.models	import Peering

class PeeringTable(tables.ModelTable):
	id		= tables.Column(sortable=False, visible=False)
	peer		= tables.Column()
	user		= tables.Column()
	key		= tables.Column(sortable=False, visible=False)

	class Meta:
		model	= Peering

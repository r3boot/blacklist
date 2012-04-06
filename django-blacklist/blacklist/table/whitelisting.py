
import django_tables	as tables
from blacklist.models	import WhiteListing

class WhiteListingTable(tables.ModelTable):
	id		= tables.Column(sortable=False, visible=False)
	ip		= tables.Column()
	hostname	= tables.Column()

	class Meta:
		model	= WhiteListing

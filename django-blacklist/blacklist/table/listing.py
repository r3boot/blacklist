
import django_tables	as tables
from blacklist.models	import Listing

class ListingTable(tables.ModelTable):
	id			= tables.Column(sortable=False, visible=False)
	ip			= tables.Column()
	reason		= tables.Column()
	sensor		= tables.Column()
	sensor_host	= tables.Column()
	timestamp	= tables.Column()
	duration	= tables.Column()
	reporter	= tables.Column()

	class Meta:
		model	= Listing

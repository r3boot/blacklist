
import django_tables	as tables
from blacklist.models	import Country

class CountryTable(tables.ModelTable):
	id	= tables.Column(sortable=False, visible=False)
	code	= tables.Column(sortable=True)
	name	= tables.Column(sortable=True)

	class Meta:
		model	= Country

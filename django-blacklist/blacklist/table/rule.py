
import django_tables	as tables
from blacklist.models	import Rule

class RuleTable(tables.ModelTable):
	id		= tables.Column(sortable=False, visible=False)
	sensor		= tables.Column()
	rule		= tables.Column()

	class Meta:
		model	= Rule

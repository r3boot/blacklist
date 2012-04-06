from django	import forms

from blacklist.models	import Rule

class SearchForm(forms.Form):
	q	= forms.CharField(max_length=1024)

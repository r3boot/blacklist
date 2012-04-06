from django	import forms

from blacklist.models	import Listing

class ListingForm(forms.Form):
	ip			= forms.CharField(max_length=39)
	reason		= forms.CharField(max_length=1024)


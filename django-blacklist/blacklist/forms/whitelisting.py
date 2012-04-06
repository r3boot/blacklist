from django	import forms

from blacklist.models	import WhiteListing

class WhiteListingForm(forms.Form):
	ip	= forms.CharField(max_length=43)
	hostname	= forms.CharField(max_length=512)

from django	import forms

class PeeringForm(forms.Form):
	hostname	= forms.CharField(max_length=512)
	ip			= forms.CharField(max_length=39)
	asnum		= forms.CharField(max_length=16)
	key			= forms.CharField(max_length=1024)

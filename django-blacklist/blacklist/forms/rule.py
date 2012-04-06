from django	import forms

from blacklist.models	import Rule

class RuleForm(forms.Form):
	rule		= forms.CharField(widget=forms.Textarea)
	sensor		= forms.CharField(max_length=256)
	pos_ip		= forms.IntegerField()
	pos_reason	= forms.IntegerField()

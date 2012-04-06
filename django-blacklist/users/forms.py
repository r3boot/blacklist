from django		import forms

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))
	prevpage = forms.CharField(widget=forms.widgets.HiddenInput())

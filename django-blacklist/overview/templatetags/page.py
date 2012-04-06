from django     import template

register = template.Library()

@register.simple_tag
def matchpage(request, pattern):
	import re
	if re.search(pattern, request.path):
		return True
	return None


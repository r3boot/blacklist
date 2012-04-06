from django	import template

from blacklist.common.ipcalc	import IPCalc

ipcalc = IPCalc()

register = template.Library()

@register.simple_tag
def itodq(i, af):
	return ipcalc.itodq(int(i), af)

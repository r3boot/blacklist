
from blacklist.backend	import whitelisting

class WhiteListing(whitelisting.WhiteListing):
	def __init__(self):
		whitelisting.WhiteListing.__init__(self)

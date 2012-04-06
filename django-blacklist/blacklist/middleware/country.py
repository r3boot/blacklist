
from blacklist.backend	import country

class Country(country.Country):
	def __init__(self):
		country.Country.__init__(self)

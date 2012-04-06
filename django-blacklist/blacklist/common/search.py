from django.db.models	import Q

from blacklist.common.ipcalc	import IPCalc

class Search:
	def __init__(self, model=None, fields=[]):
		self.model = model
		self.fields = fields
		self.operators = ["and", "or"]
		self.quotes = ["\"", "\'"]
		self.fs = "="
		self.ipcalc = IPCalc()

	def _construct_ip(self, cur_field, cur_value, is_negate):
		qset = None
		if "/" in cur_value:
			(ip, mask) = cur_value.split("/")
		else:
			ip = cur_value
			mask = None
		try:
			ip = self.ipcalc.dqtoi(ip)
		except ValueError:
			return (False, "%s is not a valid ip address" % (cur_value))

		first = eval("Q(%s__lte=\"%s\")" % (self.fields[cur_field], ip))
		if cur_field == "ip":
			last = eval("Q(ip__last__gte=\"%s\")" % (ip))
		else:
			last = eval("Q(last__gte=\"%s\")" % (ip))

		qset = (first & last)
		if mask:
			qset = qset & eval("Q(mask=\"%s\")" % (mask))

		if is_negate:
			return ~(qset)
		else:
			return (qset)

	def _construct(self, cur_field, cur_value, is_negate):
		qset_list = []
		operator_list = []
		for quote in self.quotes:
			cur_value.replace("\%s" % (quote), "")
		if cur_field in ["ip", "subnet"]:
			qset_list.append(self._construct_ip(cur_field, cur_value, is_negate))
		else:
			if is_negate:
				qset_list.append(eval("~Q(%s__icontains=\"%s\")" % (self.fields[cur_field], cur_value)))
			else:
				qset_list.append(eval("Q(%s__icontains=\"%s\")" % (self.fields[cur_field], cur_value)))
		return (qset_list, operator_list)

	def find(self, q):
		qset = None
		qset_list = []
		is_field = True
		is_value = False
		is_operator = False
		is_multiword = False
		is_negate = False
		is_ip = True
		has_quote = False

		cur_field = ""
		cur_value = ""

		operator_list = []

		for i in range(0, len(q)):
			if q[i] == self.fs:
				is_field = False
				is_value = True
				cur_field = cur_field.strip()
				if cur_field.startswith("not "):
					is_negate = True
					cur_field = cur_field[4:]
				cur_field = cur_field.strip()
				if not cur_field in self.fields.keys():
					return (False, "%s is not a valid field" % (cur_field))
				continue
			if q[i] in self.quotes:
				is_multiword = not is_multiword
				continue
			if is_field:
				cur_field += q[i]
			if is_value:
				cur_value += q[i]
			if cur_value.endswith(" and") and not is_multiword:
				cur_value = cur_value[:-4]
				for quote in self.quotes:
					cur_value.replace("\%s" % (quote), "")

				operator_list.append("and")
				(ql, ol) = self._construct(cur_field, cur_value, is_negate)
				for i in ql: qset_list.append(i)
				for i in ol: operator_list.append(i)

				is_field = True
				is_value = False
				is_negate = False
				cur_field = ""
				cur_value = ""
			if cur_value.endswith(" or") and not is_multiword:
				cur_value = cur_value[:-3]
				for quote in self.quotes:
					cur_value.replace(quote, "")

				operator_list.append("or")
				(ql, ol) = self._construct(cur_field, cur_value, is_negate)
				for i in ql: qset_list.append(i)
				for i in ol: operator_list.append(i)

				is_field = True
				is_value = False
				is_negate = False
				is_ip = False
				cur_field = ""
				cur_value = ""

		(ql, ol) = self._construct(cur_field, cur_value, is_negate)
		for i in ql: qset_list.append(i)
		for i in ol: operator_list.append(i)

		qset = qset_list[0]
		del(qset_list[0])
		for operator in operator_list:
			if operator == "and":
				qset = qset & qset_list[0]
				del(qset_list[0])
			elif operator == "or":
				qset = qset | qset_list[0]
				del(qset_list[0])

		return self.model.filter(qset)

from django.contrib.auth.models	import User

def has_user(user):
	try:
		User.objects.get(username=user)
		return True
	except User.DoesNotExist:
		return False

def get_user(username):
	username = username.strip()
	if not has_user(username):
		return (False, "User does not exist")
	return (True, User.objects.get(username=username))
	

def create_user(user, passwd, email, first_name, last_name, staff):
	if has_user(user):
		return (False, "User already exists")

	user = User.objects.create_user(user, email, passwd)
	user.first_name=first_name
	user.last_name=last_name
	user.is_staff=staff
	user.save()
	return (True, user)

def remove_user(username):
	(result, data) = get_user(username)
	if not result: return (False, data)
	data.delete()
	return (True, "User removed")


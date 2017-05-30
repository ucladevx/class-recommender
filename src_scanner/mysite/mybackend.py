from django.conf import settings
from django.contrib.auth import get_user_model

class MyBackend(object):

	def authenticate(self, username=None, password=None):
		User = get_user_model()
		# authenticate with email 
		try: 
				user = User.objects.get(email=username) 
				if user.check_password(password): 
						return user 
		except User.DoesNotExist: 
				# authentication with username 
				try: 
						user = User.objects.get(username=username) 
						if user.check_password(password): 
								return user 
				except User.DoesNotExist: 
						# neither nor succesfull, so no user exists 
						return None 

	def get_user(self, user_id):
		UserModel = get_user_model()
		try:
			user = UserModel._default_manager.get(pk=user_id)
		except UserModel.DoesNotExist:
			return None
		return user if getattr(user, 'is_active', True) else None
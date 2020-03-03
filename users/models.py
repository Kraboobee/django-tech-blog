from django.db import models
from django.contrib.auth.models import User

# Profile model for users
	# Provides a one-to-one relationship with Users. 
	# If a user is deleted, their profile will be deleted as well
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

# To-string method for Profile
	def __str__(self):
		return f'{self.user.username} Profile'

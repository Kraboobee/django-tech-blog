from django.db 					import models
from django.contrib.auth.models import User
from PIL 						import Image
import io
from django.core.files.storage 	import default_storage as storage

# Profile model for users
	# Provides a one-to-one relationship with Users. 
	# If a user is deleted, their profile will be deleted as well
class Profile(models.Model):
	user 	= models.OneToOneField(User, on_delete=models.CASCADE)
	image 	= models.ImageField(default='default.jpg', upload_to='profile_pics')

# To-string method for Profile
	def __str__(self):
		return f'{self.user.username} Profile'

	# def save(self, *args, **kwargs):
	# 	super().save(*args, **kwargs)

	# 	img = Image.open(self.image.path)

	# 	if img.height > 300 or img.width > 300:
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)

	# image resizing function
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img_read = storage.open(self.image.name, 'r')
		img = Image.open(img_read)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			in_mem_file = io.BytesIO()
			img.save(in_mem_file, format='JPEG')
			img_write = storage.open(self.image.name, 'w+')
			img_write.write(in_mem_file.getvalue())
			img_write.close()

		img_read.close()
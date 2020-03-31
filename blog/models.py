from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

YOUTUBE = 'Youtube'
DOCUMENTATION = 'Documentation'
SUBREDDIT = 'Subreddits'
FORUM = 'Forum'
BLOG = 'Blogs'
COURSE = 'Courses'
GITHUB = 'Github'
OTHER = 'Etc'
CATEGORY_CHOICES = [
	(YOUTUBE, 'YouTube Videos and Playlists'),
	(DOCUMENTATION, 'Tools and Documetation'),
	(SUBREDDIT, 'Subreddits'),
	(FORUM, 'Forums'),
	(BLOG, 'Blogs and Articles'),
	(COURSE, 'Courses'),
	(GITHUB, 'Github Repositories'),
	(OTHER, 'Other Resources'),
	('', 'Any'),
]
class Resource(models.Model):
	category = models.CharField(
		max_length = 15,
		choices = CATEGORY_CHOICES,
		default = OTHER
	)
	body = MarkdownxField()
	description = models.TextField(max_length = 100, blank = True)

	def formatted_markdown(self):
		return markdownify(self.body)

	def __str__(self):
		return self.category
	

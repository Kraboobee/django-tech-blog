from django.db 					import models
from django.utils 				import timezone
from django.contrib.auth.models import User
from django.urls 				import reverse
from markdownx.models 			import MarkdownxField
from markdownx.utils 			import markdownify


# Post model
class Post(models.Model):
	title 		= models.CharField(max_length=100)
	content 	= MarkdownxField()
	date_posted = models.DateTimeField(default=timezone.now)
	author 		= models.ForeignKey(User, on_delete=models.CASCADE)
	likes 		= models.ManyToManyField(User, related_name='post_likes')

	def formatted_markdown(self):
		return markdownify(self.content)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})


# Comment model
class Comment(models.Model):
    post 		= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user 		= models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    body 		= models.TextField()
    created_on 	= models.DateTimeField(auto_now_add=True)
    active 		= models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment on {} by {}'.format(self.created_on, self.user)


# Choices for Resource category field
YOUTUBE 		= 'Youtube'
DOCUMENTATION 	= 'Documentation'
SUBREDDIT 		= 'Subreddits'
FORUM 			= 'Forum'
BLOG 			= 'Blogs'
COURSE 			= 'Courses'
GITHUB 			= 'Github'
OTHER 			= 'Etc'

CATEGORY_CHOICES = [
	(YOUTUBE, 		'YouTube Videos and Playlists'),
	(DOCUMENTATION, 'Tools and Documetation'),
	(SUBREDDIT, 	'Subreddits'),
	(FORUM, 		'Forums'),
	(BLOG, 			'Blogs and Articles'),
	(COURSE, 		'Courses'),
	(GITHUB, 		'Github Repositories'),
	(OTHER, 		'Other Resources'),
	('', 			'Any'),
]

# Resource model
class Resource(models.Model):
	category 		= models.CharField(
		max_length 	= 15,
		choices 	= CATEGORY_CHOICES,
		default 	= OTHER
	)
	body = MarkdownxField()
	description = models.TextField(max_length = 100, blank = True)

	def formatted_markdown(self):
		return markdownify(self.body)

	def __str__(self):
		return self.category

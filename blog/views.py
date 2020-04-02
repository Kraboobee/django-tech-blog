from django import forms
from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin
)
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import (
	CreateView, 
	DeleteView,
	DetailView, 
	ListView,
	UpdateView
)
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, redirect, render
import markdown
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from .forms import CommentForm
from .models import (
	Comment,
	Post, 
	Resource
)

# Home page - A list of all posts
class PostListView(ListView):
	model 				= Post
	template_name 		= 'blog/home.html'
	context_object_name = 'posts'
	ordering 			= ['-date_posted']
	paginate_by 		= 5

# Detailed view of an individual post
class PostDetailView(DetailView):
	model 				= Post

# Form to submit a comment
class CommentForm(forms.ModelForm):

	class Meta:
		model 	= Comment
		fields 	= ('body',)

# Function to handle comment form
def add_comment_to_post(request,pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		form.instance.user = request.user
		if form.is_valid():
			comment = form.save(commit = False)
			comment.post = post
			comment.save()
			return redirect('post-detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/post_comment.html', {'form': form})

# List of all posts by a user
class UserPostListView(ListView):
	model 				= Post
	template_name 		= 'blog/user_posts.html'
	context_object_name = 'posts'
	ordering 			= ['-date_posted']
	paginate_by 		= 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

# Form to create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
	model 	= Post
	fields 	= ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

# Form to update a post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model 	= Post
	fields 	= ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

# Form to delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model 		= Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

# Function to like/unlike posts
class PostLikeAPIToggle(APIView):
	authentication_classes 	= [authentication.SessionAuthentication, ]
	permission_classes 		= [permissions.IsAuthenticated, ]

	def get(self, request, pk=None, format=None):
		post 	= get_object_or_404(Post, pk=self.kwargs.get('pk'))
		user 	= self.request.user
		liked 	= False
		updated = False
		if user.is_authenticated:
			if user in post.likes.all():
				liked 	= False
				post.likes.remove(user)
				updated = True
			else:
				liked 	= True
				post.likes.add(user)
				updated = True
			data = {
					"updated": updated,
					"liked": liked,
				}
		return Response(data)

# About, Contact, and Resource Pages
def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})

def contact(request):
	return render(request, 'blog/contact.html', {'title': 'Contact'})

def resources(request):
	return render(request, 'blog/resources.html', {'title': 'resources'})

# Lists all resources within a category
class ResourceListView(ListView):
	model 				= Resource
	template_name 		= 'blog/resource_list.html'
	context_object_name = 'resources'

	def get_queryset(self):
		results = Resource.objects.filter(Q(category__icontains=self.kwargs.get('category')))
		return results

# List of posts containing a search keyword
class SearchResultListView(ListView):
	model 				= Post
	template_name 		= 'blog/search_results.html'
	context_object_name = 'posts'
	ordering 			= ['-date_posted']
	paginate_by 		= 5

	def get_queryset(self):
		results = Post.objects.filter(
				Q(title__icontains=self.kwargs.get('q')) |
				Q(content__icontains=self.kwargs.get('q'))
			).distinct()
		return results.order_by('-date_posted')
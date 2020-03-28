from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin
)
from django.contrib.auth.models import User
from django.views.generic import (
	CreateView, 
	DeleteView,
	DetailView, 
	ListView,
	UpdateView
)
from .models import Post


# Renders the blog home and about pages

# def home(request):
# 	context = {
# 		'posts': Post.objects.all()
# 	}
# 	return render(request, 'blog/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5


class SearchResultListView(ListView):
	model = Post
	template_name = 'blog/search_results.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

	def get_queryset(self):
		results = Post.objects.filter(
			Q(title__icontains=self.kwargs.get('q')) |
			Q(content__icontains=self.kwargs.get('q'))
			).distinct()
		return results.order_by('-date_posted')

	
	# def get_queryset(query=None):
	# 	query = ""
	# 	queryset = []
	# 	queries = query.split(" ")
	# 	for q in queries:
	# 		posts = Post.objects.filter(
	# 				Q(title__icontains=q) or
	# 				Q(content__icontains=q)
	# 			).distinct()
			
	# 		for post in posts:
	# 			queryset.append(post)
	# 	return list(set(queryset))

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})

def contact(request):
	return render(request, 'blog/contact.html', {'title': 'Contact'})


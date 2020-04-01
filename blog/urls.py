from django.urls import path
from .views import (
	PostCreateView, 
	PostDetailView, 
	PostDeleteView,
    PostLikeAPIToggle,
	PostListView,
	PostUpdateView,
    ResourceListView,
    SearchResultListView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/post/<int:pk>/like', PostLikeAPIToggle.as_view(), name='post-like-api'),
    path('search/<str:q>/', SearchResultListView.as_view(), name='search-results'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('resources/', views.resources, name='resources'),
    path('resources/<str:category>/', ResourceListView.as_view(), name='resources-list'),
]

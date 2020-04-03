from .models import Comment
from django import forms

# Form to add comments to posts
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)



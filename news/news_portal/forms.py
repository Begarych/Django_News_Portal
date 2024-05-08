from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'rating', 'categories']
        title = forms.CharField(min_length=10)


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'rating', 'categories']
        title = forms.CharField(min_length=10)

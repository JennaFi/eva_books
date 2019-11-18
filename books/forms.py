from django import forms
from .models import Review
from django_starfield import Stars


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['rating', 'title', 'text']
        labels = {'title': 'Your title',
                  'text': 'Your review',
                  'Your rating': 'Your rating'}

    rating = forms.IntegerField(widget=Stars)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


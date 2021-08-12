from django import forms
from django.contrib.auth.hashers import check_password
from django.core import validators

from myapp.models import Todo
from myapp.validators import not_only_numeric_validator


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'content')

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Todo title', 'widget': 'CharField'}),
            'content': forms.Textarea(
                attrs={'placeholder': 'Todo content'}),
        }


class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username'}),
        max_length=30,)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}),
        max_length=100,
        min_length=8,
        validators=[not_only_numeric_validator])


class ProfileImageForm(forms.Form):
    image = forms.ImageField()


class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'New username'}), max_length=30, min_length=5)
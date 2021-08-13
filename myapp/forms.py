import re

from django import forms
from django.core.exceptions import ValidationError

from myapp.models import Todo
from myapp.validators import not_only_numeric_validator


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'content')

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Todo title', 'widget': 'CharField'},),
            'content': forms.Textarea(
                attrs={'placeholder': 'Todo content'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        if 'title' in cleaned_data:
            if not bool(re.match(r'^[A-Za-z0-9]*$', cleaned_data['title'])):
                raise ValidationError('Todo title can only contain letters and numbers.')

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username'}),
        max_length=30,)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}),
        max_length=100,)


class ProfileImageForm(forms.Form):
    image = forms.ImageField()


class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'New username'}), max_length=30, min_length=5)
from django import forms

from myapp.models import Todo


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
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)


class ProfileImageForm(forms.Form):
    image = forms.ImageField()
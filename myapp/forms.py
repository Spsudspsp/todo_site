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
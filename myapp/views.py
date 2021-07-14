from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
from myapp.forms import TodoForm
from myapp.models import Todo


class CompleteView(View):

    def get(self, request, pk, *args, **kwargs):
        todo = Todo.objects.get(pk=pk)
        todo.completed = True
        todo.save()
        return redirect('home page')


class UndoCompleteView(View):

    def get(self, request, pk, *args, **kwargs):
        todo = Todo.objects.get(pk=pk)
        todo.completed = False
        todo.save()
        return redirect('home page')


class ChangePasswordView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'change_password.html')


class ChangeUsernameView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'change_username.html')


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


class RegisterView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'registration.html')


class ProfilePageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'profile.html')


class TodoDetailsView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo = None

    def dispatch(self, request, *args, **kwargs):
        self.todo = Todo.objects.get(pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'todo': self.todo
        }
        return render(request, 'todo-details.html', context)


class CreateTodoView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'form': TodoForm()
        }
        return render(request, 'create-todo.html', context)

    def post(self, request, *args, **kwargs):
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home page')


class EditTodoView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo = None

    def dispatch(self, request, *args, **kwargs):
        self.todo = Todo.objects.get(pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TodoForm(instance=self.todo)
        context = {
            'form': form
        }
        return render(request, 'create-todo.html', context)

    def post(self, request, *args, **kwargs):
        form = TodoForm(request.POST, instance=self.todo)
        if form.is_valid():
            form.save()
            return redirect('home page')


class DeleteTodoView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo = None

    def dispatch(self, request, *args, **kwargs):
        self.todo = Todo.objects.get(pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TodoForm(instance=self.todo)
        for field in form.fields:
            form.fields[field].disabled = True
        context = {
            'form': form
        }
        return render(request, 'create-todo.html', context)

    def post(self, request, *args, **kwargs):
        self.todo.delete()
        return redirect('home page')


class HomePageView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'todos': Todo.objects.all()
        }
        return render(request, 'home-with-profile.html', context)
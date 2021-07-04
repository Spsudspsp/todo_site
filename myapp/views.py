from django.shortcuts import render, redirect


# Create your views here.
from myapp.models import Todo


def complete(request, pk):
    return redirect('home page')


def change_password(request):
    return render(request, 'change_password.html')


def change_username(request):
    return render(request, 'change_username.html')


def index(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'registration.html')


def profile_page(request):
    return render(request, 'profile.html')


def todo_details(request, pk):
    todo = Todo.objects.get(pk=pk)
    context = {
        'todo': todo
    }
    return render(request, 'todo-details.html', context)


def create_todo(request):
    return render(request, 'create-todo.html')


def edit_todo(request, pk):
    return render(request, 'create-todo.html')


def delete_todo(request, pk):
    return render(request, 'create-todo.html')


def homepage(request):
    context = {
        'todos': Todo.objects.all()
    }
    return render(request, 'home-with-profile.html', context)





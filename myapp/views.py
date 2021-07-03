from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'registration.html')


def profile_page(request):
    return render(request, 'profile.html')


def todo_details(request, pk):
    return render(request, 'todo-details.html')


def create_todo(request):
    return render(request, 'create-todo.html')


def edit_todo(request, pk):
    return render(request, 'create-todo.html')


def delete_todo(request, pk):
    return render(request, 'create-todo.html')


def homepage(request):
    return render(request, 'home-with-profile.html')





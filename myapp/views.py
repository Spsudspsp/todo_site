import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
from myapp.forms import TodoForm, RegistrationForm, ProfileImageForm
from myapp.models import Todo, Profile


class LogoutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


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
        context = {
            'form': RegistrationForm(),
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home page')
            return redirect('/')


class RegisterView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'form': RegistrationForm(),
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            return redirect('index')


class ProfilePageView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'profile': request.user.user_profile,
        }
        return render(request, 'profile.html', context)


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
            a = form.save(commit=False)
            a.user = request.user
            a.save()
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
            'todos': Todo.objects.filter(user=request.user)
        }
        return render(request, 'home-with-profile.html', context)


class SetProfileImageView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'form': ProfileImageForm()
        }
        return render(request, 'profile-image-upload.html', context)

    def post(self, request, *args, **kwargs):
        form = ProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user.user_profile
            if user.profile_image:
                os.remove('media/images/' + user.profile_image.name.split('/')[-1])
            user.profile_image = form.cleaned_data['image']
            user.save()
            return redirect('home page')
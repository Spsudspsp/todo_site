import os

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
from myapp.forms import TodoForm, RegistrationForm, ProfileImageForm, ChangeUsernameForm
from myapp.models import Todo, Profile


class DeleteProfileView(View):

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.user_profile.profile_image:
            os.remove('media/images/' + user.user_profile.profile_image.name.split('/')[-1])
        user.delete()
        return redirect('index')


class LogoutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


class CompleteView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.todo = Todo.objects.get(pk=kwargs['pk'])
        except Todo.DoesNotExist:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.todo.completed = True
        self.todo.save()
        return redirect('home page')


class UndoCompleteView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.todo = Todo.objects.get(pk=kwargs['pk'])
        except Todo.DoesNotExist:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.todo.completed = False
        self.todo.save()
        return redirect('home page')


class ChangePasswordView(View):
    form_class = PasswordChangeForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class(user=request.user)
        }
        return render(request, 'change_password.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, user=request.user)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'change_password.html', context)
        form.save()
        update_session_auth_hash(request, form.user)
        return redirect('profile page')


class ChangeUsernameView(View):
    form_class = ChangeUsernameForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class()
        }
        return render(request, 'change_username.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['new_username']
            user.save()
            auth_user = authenticate(username=user.username, password=user.password)
            login(request, auth_user)
            return redirect('profile page')
        return redirect('change username')


class IndexView(View):
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class(),
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home page')
            return redirect('/')


class RegisterView(View):
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class(),
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            login(request, user)
            return redirect('home page')
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
        try:
            self.todo = Todo.objects.get(pk=kwargs['pk'])
        except Todo.DoesNotExist:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'todo': self.todo
        }
        return render(request, 'todo-details.html', context)


class CreateTodoView(View):
    form_class = TodoForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class()
        }
        return render(request, 'create-todo.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            return redirect('home page')


class EditTodoView(View):
    form_class = TodoForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.todo = Todo.objects.get(pk=kwargs['pk'])
        except Todo.DoesNotExist:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.todo)
        context = {
            'form': form
        }
        return render(request, 'create-todo.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.todo)
        if form.is_valid():
            form.save()
            return redirect('home page')


class DeleteTodoView(View):
    form_class = TodoForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.todo = Todo.objects.get(pk=kwargs['pk'])
        except Todo.DoesNotExist:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.todo)
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
    form_class = ProfileImageForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class()
        }
        return render(request, 'profile-image-upload.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = request.user.user_profile
            if user.profile_image:
                os.remove('media/images/' + user.profile_image.name.split('/')[-1])
            user.profile_image = form.cleaned_data['image']
            user.save()
            return redirect('home page')
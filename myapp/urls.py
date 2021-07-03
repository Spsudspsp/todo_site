from django.urls import path

from myapp.views import index, register, profile_page, todo_details, create_todo, edit_todo, homepage, delete_todo

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='registration page'),
    path('profile/', profile_page, name='profile page'),
    path('details/<int:pk>', todo_details, name='todo details'),
    path('create/', create_todo, name='create todo'),
    path('edit/<int:pk>', edit_todo, name='edit todo'),
    path('delete/<int:pk>', delete_todo, name='edit todo'),
    path('todos/', homepage, name='home page')
]
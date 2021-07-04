from django.urls import path

from myapp.views import index, register, profile_page, todo_details, create_todo, edit_todo, homepage, delete_todo, \
    change_username, change_password, complete

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='registration page'),
    path('profile/', profile_page, name='profile page'),
    path('details/<int:pk>', todo_details, name='todo details'),
    path('create/', create_todo, name='create todo'),
    path('edit/<int:pk>', edit_todo, name='edit todo'),
    path('delete/<int:pk>', delete_todo, name='delete todo'),
    path('todos/', homepage, name='home page'),
    path('change-username/', change_username, name='change username'),
    path('change-password/', change_password, name='change password'),
    path('complete/<int:pk>', complete, name='complete todo')
]
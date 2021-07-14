from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='registration page'),
    path('profile/', views.ProfilePageView.as_view(), name='profile page'),
    path('details/<int:pk>', views.TodoDetailsView.as_view(), name='todo details'),
    path('create/', views.CreateTodoView.as_view(), name='create todo'),
    path('edit/<int:pk>', views.EditTodoView.as_view(), name='edit todo'),
    path('delete/<int:pk>', views.DeleteTodoView.as_view(), name='delete todo'),
    path('todos/', views.HomePageView.as_view(), name='home page'),
    path('change-username/', views.ChangeUsernameView.as_view(), name='change username'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change password'),
    path('complete/<int:pk>', views.CompleteView.as_view(), name='complete todo'),
    path('undo-complete/<int:pk>', views.UndoCompleteView.as_view(), name='undo complete todo'),
]
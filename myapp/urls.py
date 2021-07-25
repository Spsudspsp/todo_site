from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path

from django.conf import settings
from myapp import views
from myapp.views import SetProfileImageView, LogoutView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='registration page'),
    path('profile/', login_required(views.ProfilePageView.as_view()), name='profile page'),
    path('details/<int:pk>', login_required(views.TodoDetailsView.as_view()), name='todo details'),
    path('create/', login_required(views.CreateTodoView.as_view()), name='create todo'),
    path('edit/<int:pk>', login_required(views.EditTodoView.as_view()), name='edit todo'),
    path('delete/<int:pk>', login_required(views.DeleteTodoView.as_view()), name='delete todo'),
    path('todos/', login_required(views.HomePageView.as_view()), name='home page'),
    path('change-username/', views.ChangeUsernameView.as_view(), name='change username'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change password'),
    path('complete/<int:pk>', login_required(views.CompleteView.as_view()), name='complete todo'),
    path('undo-complete/<int:pk>', login_required(views.UndoCompleteView.as_view()), name='undo complete todo'),
    path('set-profile-image', login_required(SetProfileImageView.as_view()), name='set pfp'),
    path('logout', login_required(LogoutView.as_view()), name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
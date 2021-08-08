from django.test import SimpleTestCase
from django.urls import reverse, resolve

from myapp import views as v


class TestUrls(SimpleTestCase):

    def test_register_url_resolved(self):
        url = reverse('registration page')
        self.assertEquals(resolve(url).func.view_class, v.RegisterView)

    def test_index_url_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func.view_class, v.IndexView)

    def test_profile_url_resolved(self):
        url = reverse('profile page')
        self.assertEquals(resolve(url).func.view_class, v.ProfilePageView)

    def test_create_todo_url_resolved(self):
        url = reverse('create todo')
        self.assertEquals(resolve(url).func.view_class, v.CreateTodoView)

    def test_homepage_url_resolved(self):
        url = reverse('home page')
        self.assertEquals(resolve(url).func.view_class, v.HomePageView)

    def test_change_username_url_resolved(self):
        url = reverse('change username')
        self.assertEquals(resolve(url).func.view_class, v.ChangeUsernameView)

    def test_change_password_url_resolved(self):
        url = reverse('change password')
        self.assertEquals(resolve(url).func.view_class, v.ChangePasswordView)

    def test_det_pfp_url_resolved(self):
        url = reverse('set pfp')
        self.assertEquals(resolve(url).func.view_class, v.SetProfileImageView)

    def test_logout_url_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, v.LogoutView)

    def test_delete_profile_url_resolved(self):
        url = reverse('delete profile')
        self.assertEquals(resolve(url).func.view_class, v.DeleteProfileView)


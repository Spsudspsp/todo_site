import os

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from myapp.models import Todo, Profile


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewtestuser', password='viewtestuserpassword')

    def tearDown(self):
        self.user.delete()

    def test_index_page_GET(self):
        response = self.client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_index_page_POST_valid_credentials(self):
        response = self.client.post(reverse('index'), {
            'username': 'viewtestuser',
            'password': 'viewtestuserpassword'
        })

        # redirects to todos page if credentials are valid and user is logged
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('home page'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_index_page_POST_invalid_credentials(self):
        response = self.client.post(reverse('index'), {
            'username': 'viewtestuserinmvalid',
            'password': 'viewtestuserpasswordinvalid'
        })

        # returns to index if the credentials are invalid
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_register_page_GET(self):
        response = self.client.get(reverse('registration page'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

    def test_register_page_POST_valid_credentials(self):
        response = self.client.post(reverse('registration page'), {
            'username': 'registerpagetestuser',
            'password': 'registerpagetestuserpass'
        })
        user = User.objects.get(username='registerpagetestuser')

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('home page'))
        self.assertTrue(user)
        self.assertTrue(user.user_profile)
        self.assertFalse(user.user_profile.profile_image)

    def test_register_page_POST_invalid_credentials(self):
        response = self.client.post(reverse('registration page'), {
            'username': '',
            'password': ''
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('registration page'))

    def test_register_page_POST_invalid_credentials_numeric_password(self):
        response = self.client.post(reverse('registration page'), {
            'username': 'registerpagetestuser',
            'password': '123123123'
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('registration page'))

    def test_home_page_GET(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')
        response = self.client.get(reverse('home page'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home-with-profile.html')

    def test_profile_page_GET(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')
        response = self.client.get(reverse('profile page'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_set_profile_image_page_GET(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')
        response = self.client.get(reverse('set pfp'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile-image-upload.html')

    def test_set_profile_image_page_POST(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        self.assertFalse(self.user.user_profile.profile_image)
        response = self.client.post(reverse('set pfp'), {'image': SimpleUploadedFile(name='test_image.jpg', content=open('myapp/tests/media/images/test_image.jpg', 'rb').read(), content_type='image/jpeg')})
        self.assertRedirects(response, reverse('home page'))

        user = User.objects.get(username='viewtestuser')
        self.assertTrue(user.user_profile.profile_image)

        if user.user_profile.profile_image:
            os.remove('media/images/' + user.user_profile.profile_image.name.split('/')[-1])

    def test_set_profile_image_page_POST_invalid_data(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        self.assertFalse(self.user.user_profile.profile_image)
        response = self.client.post(reverse('set pfp'), {})
        self.assertRedirects(response, reverse('set pfp'))


    def test_create_todo_page_GET(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        response = self.client.get(reverse('create todo'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'create-todo.html')

    def test_create_todo_page_POST_valid_data(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        response = self.client.post(reverse('create todo'), {'title': 'asd', 'content': 'sdfsdfsdf'})

        self.assertTrue(Todo.objects.get(title='asd'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('home page'))

    def test_create_todo_page_POST_invalid_data(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        response = self.client.post(reverse('create todo'), {})

        self.assertFalse(Todo.objects.all())
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('create todo'))

    def test_todo_details_page_GET(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')
        todo = Todo.objects.create(title='asd', content='asd', user=self.user)

        response = self.client.get(reverse('todo details', kwargs={'pk': todo.id}))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo-details.html')

        # just in case
        todo.delete()

    def test_delete_todo_page_GET(self):

        self.client.login(username='viewtestuser', password='viewtestuserpassword')
        todo = Todo.objects.create(title='asd', content='asd', user=self.user)

        response = self.client.get(reverse('delete todo', kwargs={'pk': todo.id}))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'create-todo.html')

        # just in case
        todo.delete()

    def test_edit_todo_page_GET(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')
        todo = Todo.objects.create(title='asd', content='asd', user=self.user)

        response = self.client.get(reverse('edit todo', kwargs={'pk': todo.id}))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'create-todo.html')

        # just in case
        todo.delete()

    def test_edit_todo_page_POST(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')
        todo = Todo.objects.create(title='asd', content='asd', user=self.user)

        response = self.client.post(reverse('edit todo', kwargs={'pk': todo.id}), {'title': 'asd1', 'content': 'asd111', 'user': self.user})

        edited_todo = Todo.objects.get(title='asd1')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(edited_todo.title, 'asd1')
        self.assertEquals(edited_todo.content, 'asd111')
        self.assertRedirects(response, reverse('home page'))

        # just in case
        todo.delete()

    def test_delete_profile_page_POST(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        response = self.client.post(reverse('delete profile'))

        self.assertRedirects(response, reverse('index'))
        self.assertFalse(User.objects.all())
        self.assertFalse(Profile.objects.all())
        self.assertEquals(response.status_code, 302)

    def test_complete_todo_page_GET(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')
        todo = Todo.objects.create(title='asd', content='asd', user=self.user)

        self.assertFalse(todo.completed)
        response = self.client.get(reverse('complete todo', kwargs={'pk': todo.id}))

        edited_todo = Todo.objects.get(title='asd', user=self.user)
        self.assertTrue(edited_todo.completed)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('home page'))

        # just in case
        todo.delete()

    def test_undo_complete_todo_page_GET(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')
        todo = Todo.objects.create(title='asd', content='asd', completed=True, user=self.user)

        self.assertTrue(todo.completed)
        response = self.client.get(reverse('undo complete todo', kwargs={'pk': todo.id}))

        edited_todo = Todo.objects.get(title='asd', user=self.user)
        self.assertFalse(edited_todo.completed)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('home page'))

        # just in case
        todo.delete()

    def test_change_username_page_GET(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        response = self.client.get(reverse('change username'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_username.html')

    def test_change_username_page_POST_valid_data(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        response = self.client.post(reverse('change username'), {'new_username': 'newtestusername'})

        user = User.objects.first()

        self.assertEquals(user.username, 'newtestusername')
        self.assertRedirects(response, reverse('profile page'))
        self.assertEquals(response.status_code, 302)

    def test_change_username_page_POST_invalid_data(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        response = self.client.post(reverse('change username'), {'new_username': 'newtestusernamenewtestusernamenewtestusernamenewtestusernamenewtestusernamenewtestusernamenewtestusername'})

        user = User.objects.first()

        self.assertEquals(user.username, 'viewtestuser')
        self.assertRedirects(response, reverse('change username'))
        self.assertEquals(response.status_code, 302)

    def test_change_password_page_GET(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        response = self.client.get(reverse('change password'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

    def test_change_password_page_POST_valid_data(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        response = self.client.post(reverse('change password'), {
            'old_password': 'viewtestuserpassword',
            'new_password1': 'newtestpassword',
            'new_password2': 'newtestpassword'
        })

        self.assertTrue(self.client.login(username='viewtestuser', password='newtestpassword'))
        self.assertRedirects(response, reverse('profile page'))

    def test_change_password_page_POST_invalid_data(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')

        response = self.client.post(reverse('change password'), {
            'old_password': 'viewtestuserpassword',
            'new_password1': '',
            'new_password2': ''
        })

        self.assertFalse(self.client.login(username='viewtestuser', password=''))
        self.assertTrue(self.client.login(username='viewtestuser', password='viewtestuserpassword'))
        self.assertRedirects(response, reverse('change password'))

    def test_change_password_page_POST_invalid_data2_numeric_only_password(self):
        self.client.login(username='viewtestuser', password='viewtestuserpassword')
        response = self.client.post(reverse('change password'), {
            'old_password': 'viewtestuserpassword',
            'new_password1': '890890890',
            'new_password2': '890890890'
        })

        self.assertFalse(self.client.login(username='viewtestuser', password='890890890'))
        self.assertTrue(self.client.login(username='viewtestuser', password='viewtestuserpassword'))
        self.assertRedirects(response, reverse('change password'))
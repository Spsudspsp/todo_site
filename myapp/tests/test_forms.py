from io import StringIO

from PIL import Image
from django.contrib.auth.models import User
from unittest import TestCase

from django.core.files import File

from TodoProject import settings
from myapp import forms as f
from django.core.files.uploadedfile import SimpleUploadedFile


class TestForms(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='unittestuser', password='unittestuserpass')

    def tearDown(self):
        self.user.delete()

    def test_todo_form_valid_data(self):
        form = f.TodoForm(data={
            'title': 'title',
            'content': 'content',
            'completed': False,
            'user': self.user
        })

        self.assertTrue(form.is_valid())

    def test_todo_form_invalid_data(self):
        form = f.TodoForm(data={})

        self.assertFalse(form.is_valid())

    def test_registration_form_valid_data(self):
        form = f.RegistrationForm(data={
            'username': 'asdasdasd',
            'password': 'asdasdasd1'
        })

        self.assertTrue(form.is_valid())

    def test_registration_form_invalid_data(self):
        form = f.RegistrationForm(data={})

        self.assertFalse(form.is_valid())

    def test_registration_form_invalid_data_numeric_password(self):
        form = f.RegistrationForm(data={
            'username': 'asdasdasd',
            'password': '11111111'
        })

        self.assertFalse(form.is_valid())

    def test_profile_image_form_invalid_data(self):
        form = f.ProfileImageForm(data={})

        self.assertFalse(form.is_valid())

    def test_change_username_form_valid_data(self):
        form = f.ChangeUsernameForm(data={'new_username': 'boiler'})

        self.assertTrue(form.is_valid())

    def test_change_username_form_invalid_data(self):
        form = f.ChangeUsernameForm()

        self.assertFalse(form.is_valid())

    def test_image_upload_form_valid_data(self):
        form = f.ProfileImageForm({}, {'image': SimpleUploadedFile(name='test_image.jpg', content=open('myapp/tests/media/images/test_image.jpg', 'rb').read(), content_type='image/jpeg')})
        print(form.errors)

        self.assertTrue(form.is_valid())
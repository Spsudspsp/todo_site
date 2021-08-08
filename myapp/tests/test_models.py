from unittest import TestCase

from django.contrib.auth.models import User

from myapp.models import Todo


class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='koledsk1', password='kolepassword1')
        self.todo = Todo.objects.create(title='asd', content='ooo', user=self.user)

    def test_todo_initialize(self):
        self.assertEqual(self.todo.title, 'asd')
        self.assertEqual(self.todo.content, 'ooo')
        self.assertEqual(self.todo.user, self.user)
        self.assertFalse(self.todo.completed)

    def test_todo_complete(self):
        self.todo.completed = True
        self.assertTrue(self.todo.completed)

    def test_undo_todo_complete(self):
        self.todo.completed = False
        self.assertFalse(self.todo.completed)

    def tearDown(self):
        self.user.delete()
        self.todo.delete()
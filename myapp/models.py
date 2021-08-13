from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from myapp.validators import no_special_characters_validator


class Todo(models.Model):
    title = models.CharField(max_length=20, validators=[no_special_characters_validator])
    content = models.TextField(max_length=500,)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_image = models.ImageField(upload_to='images', blank=True)
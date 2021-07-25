from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from myapp.models import Profile


@receiver(post_save, sender=User)
def userprofile_signal(sender, instance: User, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
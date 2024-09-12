from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    current_year = models.IntegerField()

    def __str__(self):
        return self.user.username


@receiver(post_delete, sender=Profile)
def delete_user_with_profile(sender, instance, **kwargs):
    # Delete the user when the profile is deleted
    instance.user.delete()

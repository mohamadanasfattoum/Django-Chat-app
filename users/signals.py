from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def user_postsave(sender, instance, created, **kwargs):
    user = instance
    # Check if the user is created
    # and if the profile does not exist
    # If the user is created, create a profile
    # If the user is not created, do nothing
    if created:
        Profile.objects.create(
            user=user,
                               )


@receiver(pre_save, sender=User)
def user_presave(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()
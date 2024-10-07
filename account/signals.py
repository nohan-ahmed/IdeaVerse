from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserInfo

# Django signals can listen to the post_save event when a new User is created and automatically create a corresponding UserInfo instance.
@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    # Check if the User instance was just created or not.
    if created:
        # Automatically create a UserInfo when a new User is created.
        UserInfo.objects.create(user=instance)
        


# =================================================
# Notes:- for django signals
# =================================================
# pre_save and post_save: Triggered before or after a model instance is saved.
# pre_delete and post_delete: Triggered before or after a model instance is deleted.
# Yes, you need to ensure that your Django signal is properly registered in your apps.py file's ready()
# -------------------------------------------------
# sender হলো সেই model জার কনো instance কে save() করলে আমদের receiver function টা triggered হবে। অ্যান্ড instance হলো সে যাকে save() করা হয়েছে।
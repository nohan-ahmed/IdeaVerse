import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import GENDER_TYPE
from .managers import Manager
from .utils import user_directory_path
# Create custom user models here.

class User(AbstractUser):
    # Add extra fields for Custom user model
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    email = models.EmailField(max_length=250, unique=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    brith_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50,choices=GENDER_TYPE)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =['email']
    
    objects = Manager()
    
    def __str__(self) -> str:
        return super().__str__()

class UserInfo(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='user_info')
    location = models.CharField( max_length=250)
    study_at = models.CharField(max_length=250, null=True, blank=True)
    website = models.CharField(max_length=250, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s info"

class Follow(models.Model):
    follower = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following') # Prevent the same user from following another user multiple times
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

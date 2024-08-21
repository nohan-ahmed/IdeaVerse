import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import GENDER_TYPE
from .managers import Manager
# Create custom user models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'account/media/user_{instance.id}/{filename}'

class User(AbstractUser):
    # Add extra fields for Custom user model
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    email = models.EmailField(max_length=250, unique=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    brith_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50,choices=GENDER_TYPE)
    bio = models.TextField(null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =['email']
    
    objects = Manager()
    
    def __str__(self) -> str:
        return super().__str__()
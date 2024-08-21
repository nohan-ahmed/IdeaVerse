from typing import Any
from django.contrib.auth.models import BaseUserManager


class Manager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_feilds):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_feilds)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password=None, **extra_feilds):
        extra_feilds.setdefault("is_staff", True)
        extra_feilds.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_feilds)

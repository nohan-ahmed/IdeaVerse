from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "is_staff", "is_superuser", "is_active"]
    search_fields = ["id", "username", "gender", "email", "phone"]

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Follow, UserInfo
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.

# Ensure that the admin form (CustomUserCreationForm) or any form used for creating users is properly calling set_password().
# Ensure the CustomUserAdmin in the Django admin is using the correct forms (CustomUserCreationForm for adding new users).
# Never directly assign the password to user.password, always use set_password().
# If your CustomUser model overrides the save() method, ensure it does not interfere with the password hashing.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm  # Use custom creation form for adding new users
    form = CustomUserChangeForm  # Use your custom change form

    list_display = ('id', "username", "email", "gender", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser", "gender")

    # Define fieldsets for adding new users
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )
    
    # Define fieldsets for changing user info
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "profile_image", "phone", "gender")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


    search_fields = ("username", "email")
    ordering = ("email",)

    
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["id",'user', "location", "study_at", "created_at"]
    search_fields = ["id",'user', "location", "study_at", "created_at"]
    
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["id", "follower", "following", "created_at"]
    search_fields = ["id", "follower", "following", "created_at"]
    
    def follwer(self, obj):
        return obj.follower
    
    def following(self, obj):
        return obj.following
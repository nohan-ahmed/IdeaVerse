from django.contrib import admin
from .models import User, Follow, UserInfo


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "is_staff", "is_superuser", "is_active"]
    search_fields = ["id", "username", "gender", "email", "phone"]
    
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
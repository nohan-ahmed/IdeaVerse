from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'category']
    search_fields = ['id', 'user', 'title', 'category']

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post']
    search_fields = ['id', 'post']

@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post']
    def post(self, obj):
        return obj.post
    
@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post']

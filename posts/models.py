from django.db import models
from account.models import User
from categories.models import Category
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='posts')
    thumbnail = models.ImageField(upload_to=None)
    title = models.CharField(max_length=250)
    content = models.TextField()# This will store the HTML content
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Image(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=None)
    
    def __str__(self) -> str:
        return f'{self.id}'
    
    
class Like(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='likes')
    likes = models.IntegerField()
    def __str__(self) -> str:
        return f'{self.id}'

class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    content  = models.CharField(max_length=250)
    
    def __str__(self) -> str:
        return f'{self.id}'
    

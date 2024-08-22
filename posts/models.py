from django.db import models
from account.models import User
from categories.models import Category
from .utils import user_directory_path
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='posts')
    thumbnail = models.ImageField(upload_to=user_directory_path)
    title = models.CharField(max_length=250)
    content = models.TextField()# This will store the HTML content
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # post.like_count() returns the total number of Like records related to that particular Post
    def like_count(self):
        # Here, related_name='likes' allows you to access the related Like instances from a Post instance using self.likes.
        return self.likes.count()

    # It returns True if the user has liked the post, and False otherwise.
    def is_liked_by_user(self, user):
        return self.likes.filter(user=user).exists()

    def __str__(self):
        return self.title

class Image(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=user_directory_path)
    # Alt text is used where the image does not load for some reason. This text will be displayed on the user display.
    alternative_text = models.CharField( max_length=100, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f'{self.id}'

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.post.title}"

class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    content  = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f'{self.id}'

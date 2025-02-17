from django.db import models
from account.models import User
from categories.models import Category
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='posts')
    thumbnail = models.ImageField(upload_to='posts/media/images/', null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()# This will store the HTML content
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # post.like_count() returns the total number of Like records related to that particular Post
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts')
    def like_count(self):
        # Here, related_name='likes' allows you to access the related Like instances from a Post instance using self.likes.
        return self.likes.count()

    def __str__(self):
        return self.title

"""
আমরা যদি একটা পোস্ট এর মধ্যে অনেক গুল ইমেজ কে ব্যবহার করতে চাই তাহলে আমদের Image কে handle করার জন্য আলাদা model create করতে হবে যে model এর সাথে পোস্ট model এর relationship থাকবে।
user আমদের frontend থেকে markdown format এ post এর content এর মধ্যে মধ্যে ডাটা গুল পাঠাবে। যেটার মধ্যে আমদের পোস্ট এর জন্য upload করা সবগুল ইমেজ এর লিংক থাকবে যেখান থেকে ইমেজ গুল load hobe.
"""
class Image(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/media/images/')
    # Alt text is used where the image does not load for some reason. This text will be displayed on the user display.
    alternative_text = models.CharField( max_length=100, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f'{self.id}'

class Like(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
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

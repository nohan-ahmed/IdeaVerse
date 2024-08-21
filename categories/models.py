from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug=models.SlugField(max_length=200)
    
    def __str__(self) -> str:
        return self.name
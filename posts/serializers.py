from rest_framework import serializers
from .models import Post, Image, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "author": {"read_only": True},
            "created_at": {"read_only": True},
        }
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "uploaded_at": {"read_only": True},
        }

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        extra_kwargs = {
            "created_at": {"read_only": True},
            "user": {"read_only": True},
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }

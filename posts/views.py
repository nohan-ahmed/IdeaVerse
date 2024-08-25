from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle, AnonRateThrottle
from .paginations import CustomPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from . import models
from . import serializers
from .throttling import PostRateThrottle # custom throttling
from account.models import User
# Create your views here.

class PostView(ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope  = 'My_post'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'category'] # This means user can filter based on author, category fields, 
    search_fields  = ['title']
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        """
        perform_create Method: This method is a hook provided by Django REST Framework's ModelViewSet. 
        It allows you to customize the creation of a model instance without completely overriding the create method.
        """
        
        """
        Setting the author: By calling serializer.save(author=self.request.user), you automatically set the author field to the currently authenticated user when a post is created.
        This ensures that the author is set correctly and prevents users from tampering with the field
        """
        serializer.save(author=self.request.user)

class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user']
    search_fields = ['user']
    def post(self, request, format=None):
        serializer = serializers.LikeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            post = serializer.validated_data.get('post')

            # Check if the user has already liked the post
            like = models.Like.objects.filter(user=user, post=post).first()
            """
            like = models.Like.objects.filter(user=user, post=post).first() checks if there's already a like from the user on this post.
            Using .first() retrieves the first matching record or returns None if no match is found.
            """
            if not like:
                # Create a new like instance
                new_like = models.Like.objects.create(user=user, post=post)
                return Response({'like': 'Liked'}, status=status.HTTP_201_CREATED)
            else:
                # Unlike (delete the existing like)
                like.delete()
                return Response({'like': 'Unlike successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageAPIView(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle]
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields =['post']
     
    
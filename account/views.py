from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from itertools import chain
# DRF
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# custom moduls
from .models import User, Follow, UserInfo
from . import serializers
from .utils import (
    send_verification_email,
    get_tokens_for_user,
)
from .permissions import IsOwnerOrReadOnly, UserInfoIsOwnerOrReadOnly, IsOwner
from .paginations import UserPageNumberPagination
# Create your views here.

class UserRegistrationView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'RegistrationAPI'
    def post(self, request, format=None):
        serializer = serializers.RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data.setdefault('is_active', False)
            user = serializer.save()
            send_verification_email(user, request=request)
            return Response({'message':"Registration successfully please confirm the email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'RegistrationAPI'
    def get(self, request, uid, token, format=None):
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User with this Uid does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # validate the token
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # Generate JWT token
            token = get_tokens_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'ProfileAPI'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['first_name', 'last_name','gender']
    search_fields = ['id','username','email','first_name', 'last_name','gender']
    pagination_class = UserPageNumberPagination
    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        # Serialize the followers and following
        followers = serializers.FollowerSerializer(user.followers.all(), many=True)
        following = serializers.FollowerSerializer(user.following.all(), many=True)
        
        return Response({
            'user': serializer.data, 
            'followers':followers.data, 
            'following': following.data
        }, status=status.HTTP_200_OK)

class PasswordChangeView(APIView):
    permission_classes = [IsOwner]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'PasswordChangeAPI'
    def post(self, request,format=None):
        # If you want to pass additional data to the serializer class, you can pass as a context data
        serializer = serializers.PasswordChangeSerializer(data= request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            message = render_to_string('./account/change_password_email.html', {
                'user':user,
                'time':{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
            })

            subject = "Your Password Has Been Changed"
            send_mail(subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [request.user.email])
            return Response({'Message':'Passwrod changed successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'PasswordResetAPI'
    def post(self, request, format=None):
        serializer = serializers.PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email') 
            user = User.objects.get(email=email)

            # Generate a password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create the password reset link
            reset_link = f"{request.build_absolute_uri('/user/api/reset-password/confirm/')}{uid}/{token}/"

            # Send the email
            subject = "Password Reset Confirmation"
            message = render_to_string("./account/password_rest_request_email.html",{
                    "user": user,
                    "reset_password_link": reset_link,
                },
            )

            send_mail(subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [user.email])
            return Response({"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'PasswordResetAPI'
    
    def post(self, request, uid, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            serializer = serializers.PasswordResetConfirmSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user.set_password(serializer.validated_data.get('new_password'))
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)

# Notes for Logout in JWT.
"""
To implement a logout feature in Django Rest Framework (DRF) using JSON Web Tokens (JWT), 
you need to handle JWT token invalidation. Unlike session-based authentication, JWT is stateless, 
which means that once a token is generated, it cannot be "deleted" on the server side. 
However, there are several strategies to implement a logout feature using JWT in DRF:
"""

# 1.Token Blacklisting

"""
This is the most common approach to implement logout with JWTs. It involves maintaining a 
blacklist of tokens that have been invalidated. When a user logs out, the token is added to the blacklist, 
and subsequent requests using this token will be rejected.
"""

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)  # Ensures only authenticated users can access this view.
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'LogoutAPI'
    def post(self, request):
        # Initialize the LogoutSerializer with the request data (which should contain the 'refresh' token).
        serializer = serializers.LogoutSerializer(data=request.data)

        # Validate the serializer data.
        if serializer.is_valid(raise_exception=True):
            # If validation is successful, extract the 'refresh' token from the validated data.
            try:
                refresh_token = serializer.validated_data['refresh']
                
                # Create a RefreshToken instance from the provided token.
                token = RefreshToken(refresh_token)
                
                # Blacklist the refresh token, effectively logging out the user.
                token.blacklist()
                
                # Return a success response with HTTP 205 status code indicating that the client should reset the view.
                return Response({"message": "User logout successfully."}, status=status.HTTP_205_RESET_CONTENT)
            
            except Exception as e:
                # If there is an error (e.g., an invalid token), return a 400 Bad Request response.
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        # If serializer data is not valid, return the errors with a 400 Bad Request response.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoCreateAPIView(generics.CreateAPIView):
    throttle_classes =[ScopedRateThrottle]
    throttle_scope = 'RegistrationAPI'
    queryset = UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer
    permission_classes =[IsAuthenticated]

class UserInfoRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'ProfileAPI'
    queryset  = UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer
    permission_classes = [UserInfoIsOwnerOrReadOnly]

class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    def post(self, request, format=None):

        serializer = serializers.FollowerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        follower_user= request.user
        following_user = serializer.validated_data.get('following')
        # if the follower already following this user it will return the follow model's instance. otherwise None.
        already_following = Follow.objects.filter(follower= follower_user, following = following_user)
        
        if already_following:
            # Unfollow if the follower already following.
            already_following.delete() # it will be remove this instance from the follow model 
            return Response({'message':f'{follower_user} Unfollow {following_user}'}, status=status.HTTP_204_NO_CONTENT)
        
        """
        এখানে আমরা একটা new follow model's instance create করতেছি। কিন্তু আমরা আমাদের FollowerSerializer এর মধ্যে follower field কে read only করে রেখেছি।
        Because আমদের follower কে আমারা backend থেকে handle করবো। Because of আমদের follower request.user নিজেই। FollowerSerializer.save() কে call করবো আমদের follower model error দিবে কারন সে দুইটা field নেয় follower and following.
        আর follower কে read_only রাখার কারনে frontend থেকে ডাটা গুলো আসেই নাই। তাই আমরা সেটা কে save() method এর মধ্যে দিয়ে দিলাম।
        Basically যদি কনো field কে আমরা backend থেকে handle করতে চাই সেটা আমরা serializer.save() এর মধ্যে দিয়ে দিবো।
        """
        serializer.save(follower=follower_user) # if follwer don't following this account it will create new instance for follow model
        return Response({'message':f'{follower_user} following {following_user}'}, status=status.HTTP_201_CREATED)

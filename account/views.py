from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
# DRF
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# custom moduls
from .models import User
from . import serializers
from .utils import (
    send_verification_email,
    get_tokens_for_user,
)
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = serializers.RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data.setdefault('is_active', False)
            user = serializer.save()
            send_verification_email(user=user)
            return Response({'message':"Registration successfully please confirm the email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request,uid, token, format=None):
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

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

class PasswordChangeView(APIView):
    def put(self, request,format=None):
        # If you want to pass additional data to the serializer class, you can pass as a context data
        serializer = serializers.PasswordChangeSerializer(data= request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = f"""
                Hi {request.user.username},

                Your password was successfully changed on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}. 

                If you did not make this change, please secure your account immediately by visiting the following link:
                [Secure Your Account](#)

                Thank you,
                The Team Meduam.com
                """

            subject = "Your Password Has Been Changed"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email])
            return Response({'Message':'Passwrod changed successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    def post(self, request, format=None):
        serializer = serializers.PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            user = User.objects.get(email=email)

            # Generate a password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create the password reset link
            reset_link = f"{request.build_absolute_uri('/user/api/reset-password/confirm/')}{uid}/{token}/"

            # Send the email
            subject = "Password Reset Request"
            message = f"""
                'user': {user},
                'reset_link': {reset_link},"""

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            return Response({"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            serializer = serializers.PasswordResetConfirmSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)


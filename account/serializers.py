from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, Follow, UserInfo


class RegistrationSerializer(serializers.ModelSerializer):
    # Add confirm_password field for just validation purposes
    confirm_password = serializers.CharField(style={'input_type': 'password'},write_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email','brith_date','gender' , 'password', 'confirm_password']
        extra_kwargs = {
            "password": {"write_only": True},
        }
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        # Check that the password and confirm_password match.
        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm password doesn't match!")
        
        try:
            validate_password(password=password, user=None)
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return super().validate(attrs)
        
    # To create a new user instance you need to override the create() method for the RegisterSerializer class.
    def create(self, validated_data):
        """
            Remove confirmed password from validated_data. Because confirm_password is not a user model field.
            This is a serializer level field used only for validation purposes.so if you don't remove if before create a user it will raise an exeption.
        """
        validated_data.pop('confirm_password') 
        # And use this approach below to create new user instance, with proper password hashing.
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','profile_image','username', 'first_name', 'last_name','email','brith_date','gender']
        extra_kwargs = {'id':{'read_only':True}}

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    new_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)

    def validate_old_password(self, value):
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('New password and confirm password do not match.')
        if attrs.get('new_password') == attrs.get('old_password'):
            raise serializers.ValidationError("old password and new password are the same.")
        
        validate_password(attrs.get('new_password'), user=self.context.get('request').user)
        return attrs

    def save(self, **kwargs):
        user = self.context.get('request').user
        new_password = self.validated_data.get('new_password')  # Accessing the new password from validated data
        user.set_password(new_password)
        user.save()
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=250)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email does not exist")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('New password and confirm password do not match.')
        validate_password(attrs.get('new_password'), user=None)
        return attrs

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
        extra_kwargs = {
            "follower": {"read_only": True},
            "created_at": {"read_only": True},
        }

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

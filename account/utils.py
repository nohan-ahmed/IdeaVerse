from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken


def send_verification_email(user, request):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        verification_link = f"{request.build_absolute_uri('/user/api/verify-email/')}{uid}/{token}/"
        subject = 'Email Verification'
        
        # Render the HTML template with context
        message = render_to_string('./account/verification_mail.html',{
            'user': user,
            'verification_link': verification_link,
        })
        
        send_mail(subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [user.email])

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# this function genarate dynamic path to store users profile images
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'account/media/user_{instance.id}/{filename}'
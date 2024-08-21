from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView # import JWT's default views for authentication.
from . import views

router = DefaultRouter()
router.register('profile', views.ProfileView, basename='profile')
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='verify-email'),
    path('login/', TokenObtainPairView.as_view(), name='login'), # TokenObtainPairView Returns an access and refresh token if your credential is valid.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Allows the client to refresh the access token using the refresh token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('verify-email/<uid>/<token>/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('change-password/', views.PasswordChangeView.as_view(), name='verify-email'),
    path('reset-password/', views.PasswordResetRequestView.as_view(), name='reset-password'),
    path('reset-password/confirm/<uid>/<token>/', views.PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path("", include(router.urls)),
]

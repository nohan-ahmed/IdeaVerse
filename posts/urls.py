from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostView)
urlpatterns = [
    path('like/', views.LikeAPIView.as_view(), name='like'),
    # path('like/<int:pk>/', views.LikeAPIView.as_view(), name='likes'),
    path("", include(router.urls)),
]

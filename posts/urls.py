from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostView)
router.register('image', views.ImageAPIView)
router.register('comments', views.CommentAPIView)
urlpatterns = [
    path('like/', views.LikeAPIView.as_view(), name='like'),
    path("", include(router.urls)),
]

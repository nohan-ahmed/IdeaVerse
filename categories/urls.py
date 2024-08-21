from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.CategoryAPIView.as_view(), name='category')
]

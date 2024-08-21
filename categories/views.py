from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer
from rest_framework.generics import RetrieveAPIView
# from rest_framework.permissions import 
# Create your views here.

class CategoryAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
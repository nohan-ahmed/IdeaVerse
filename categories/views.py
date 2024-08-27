from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
# from rest_framework.permissions import 
# Create your views here.

class CategoryAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['slug', 'id']
    
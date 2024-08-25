from rest_framework.pagination import PageNumberPagination 

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 3 # default_limit
    page_size_query_param = 'limit'
    max_page_size = 100 # maximum limits 
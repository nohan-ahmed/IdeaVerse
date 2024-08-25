from rest_framework.pagination import PageNumberPagination
class UserPageNumberPagination(PageNumberPagination):
    page_size = 10 # Default limit per page
    page_size_query_param = 'limit' # Dynamic limit per page.
    max_page_size = 100 # Maximum page limit. 
    
from rest_framework import permissions, filters
from rest_framework.pagination import PageNumberPagination

class CustomPernission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS':['%(app_label)s.view_%(model_name)s'],
        'HEAD':['%(app_label)s.view_%(model_name)s'],
        'POST':['%(app_label)s.add_%(model_name)s'],
        'PUT':['%(app_label)s.change_%(model_name)s'],
        'PATCH':['%(app_label)s.change_%(model_name)s'],
        'DELETE':['%(app_label)s.delete_%(model_name)s']
    }

class PaginationPage(PageNumberPagination):
    # Количестов элементов на странице
    page_size = 10 
    page_size_query_param = "page_size"


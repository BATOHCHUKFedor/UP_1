from django.urls import path
from .views import *

urlpatterns = [
    path('info/', info_view, name='info_view'),
    path('main/', main_view, name='main_view'),
    path('contacts/', contacts_view, name='contacts_view'),
    path('our_whereabouts/', our_whereabouts_view, name='our_whereabouts_view'),
    path('products/', products_view, name='products_view'),
    path('categories/', categories_view, name='categories_view'),
    path('all_products/', all_products_view, name='all_products_view'),
    path('cart/', cart_view, name='cart_view'),
]

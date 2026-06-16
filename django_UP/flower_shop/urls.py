from django.urls import path
from .views import *

urlpatterns = [
    path('info/', info_view, name='info_view'),
    path('main/', main_view, name='main_view'),
    path('contacts/', contacts_view, name='contacts_view'),
    path('our_whereabouts/', our_whereabouts_view, name='our_whereabouts_view'),
    path('categories/', categories_view, name='categories_view'),
    path('all_products/',  FlowersListView.as_view(), name='all_products_view'),
    path('orders/', user_orders_view, name='user_orders'),

    path('flowers/<int:pk>/', FlowersDetailView.as_view(), name='flowers_detail'),
    path('flowers/create/', FlowersCreateView.as_view(), name="flowers_create"),
    path('flowers/<int:pk>/update', FlowersUpdateView.as_view(), name="flowers_update"),
    path('flowers/<int:pk>/delete', FlowersDeleteView.as_view(), name="flowers_delete"),
    
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='categories_detail'),
    path('categories/create/', CategoryCreateView.as_view(), name="categories_create"),
    path('categories/<int:pk>/update', CategoryUpdateView.as_view(), name="categories_update"),
    path('categories/<int:pk>/delete', CategoryDeleteView.as_view(), name="categories_delete"),

    path('collections/<int:pk>/', CollectionDetailView.as_view(), name='collections_detail'),
    path('collections/create/', CollectionCreateView.as_view(), name="collections_create"),
    path('collections/<int:pk>/update', CollectionUpdateView.as_view(), name="collections_update"),
    path('collections/<int:pk>/delete', CollectionDeleteView.as_view(), name="collections_delete"),

    path('promocodes/', PromoCodeListView.as_view(), name='promocodes_list'),
    path('promocodes/<int:pk>/', PromoCodeDetailView.as_view(), name='promocodes_detail'),
    path('promocodes/create/', PromoCodeCreateView.as_view(), name="promocodes_create"),
    path('promocodes/<int:pk>/update', PromoCodeUpdateView.as_view(), name="promocodes_update"),
    path('promocodes/<int:pk>/delete', PromoCodeDeleteView.as_view(), name="promocodes_delete"),

    path('suppliers/', SupplierListView.as_view(), name='suppliers_list'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view(), name='suppliers_detail'),
    path('suppliers/create/', SupplierCreateView.as_view(), name="suppliers_create"),
    path('suppliers/<int:pk>/update', SupplierUpdateView.as_view(), name="suppliers_update"),
    path('suppliers/<int:pk>/delete', SupplierDeleteView.as_view(), name="suppliers_delete"),

    path("login/",  login_user, name='login_page'),
    path("registration/",  registration_user, name='registration_page'),
    path("logout/",  logout_user, name='logout_page'),
]

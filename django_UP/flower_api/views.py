from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets, filters
from flower_shop.models import *
from .permission import *


class CategoryViewSet(viewsets.ModelViewSet):
    # Как хотим выводить данные
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [CustomPernission]
    pagination_class = PaginationPage

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializers
    permission_classes = [CustomPernission]
    pagination_class = PaginationPage

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers
    permission_classes = [CustomPernission]
    pagination_class = PaginationPage

class FlowersViewSet(viewsets.ModelViewSet):
    queryset = Flowers.objects.all()
    serializer_class = FlowersSerializers
    permission_classes = [CustomPernission]
    pagination_class = PaginationPage
    # Возможность фильтрации в url
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'color', 'category__name', 'supplier__name']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [CustomPernission]
    pagination_class = PaginationPage

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializers
    permission_classes = [CustomPernission]
    pagination_class = PaginationPage

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [CustomPernission]
    pagination_class = PaginationPage

class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCode
    permission_classes = [CustomPernission]
    pagination_class = PaginationPage
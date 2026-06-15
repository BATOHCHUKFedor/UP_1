from rest_framework import serializers
from flower_shop.models import *

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
            "description"
        ]

class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "name",
            "description"
        ]

class SupplierSerializers(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            "name",
            "contact_person",
            "phone",
            "email",
            "address"
        ]

class FlowersSerializers(serializers.ModelSerializer):
    price = serializers.DecimalField(label="Цена", max_digits=10, decimal_places=2)
    class Meta:
        model = Flowers
        fields = [
            "name",
            "description",
            "price",
            "height_cm",
            "color",
            "photo",
            "create_date",
            "is_exists",
            "category",
            "collection",
            "supplier"
        ]

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "user",
            "status",
            "created_at",
            "total_price",
            "delivery_address",
            "comment",
        ]

class OrderItemSerializers(serializers.ModelSerializer):
    price = serializers.DecimalField(label="Цена", max_digits=10, decimal_places=2)
    class Meta:
        model = OrderItem
        fields = [
            "quantity",
            "price",
            "order",
            "flower"
        ]

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "rating",
            "text",
            "created_at",
            "flower",
            "user"
        ]

class PromoCodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = [
            "code",
            "discount_percent",
            "valid_from",
            "valid_to",
            "is_active"
        ]
from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description', 'photo']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'address']


class FlowersForm(forms.ModelForm):
    class Meta:
        model = Flowers
        fields = [
            'name', 'description', 'price', 'height_cm', 'color',
            'photo', 'is_exists', 'category', 'collection', 'supplier'
        ]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'comment']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['flower', 'quantity']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text'] 


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ['code', 'discount_percent', 'valid_from', 'valid_to', 'is_active']

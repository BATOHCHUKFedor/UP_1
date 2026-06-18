from django import forms

from flower_shop.models import Order

class CartAddProductForm(forms.Form):
    count = forms.IntegerField(min_value=1, initial=1, label="Количество",
                               widget=forms.NumberInput(attrs={'class':'form-control'}))
    reload = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'comment']
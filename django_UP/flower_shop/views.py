from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import * 
from django.urls import reverse_lazy
from .forms import *
import random
from django.contrib import messages
from django.utils import timezone

def main_view(request):
    available_flowers = list(Flowers.objects.filter(is_exists=True))

    popular_flowers = random.sample(available_flowers, min(len(available_flowers), 3))
    return render(request, "main.html", {"popular_flowers": popular_flowers})

def info_view(request):
    return render(request, "info.html")

def contacts_view(request):
    return render(request, "contacts.html")

def our_whereabouts_view(request):
    return render(request, "our_whereabouts.html")

def products_view(request):
    return render(request, "products.html")

def cart_view(request):
    return render(request, "cart.html")

def categories_view(request):
    category_list = Category.objects.all()
    collections_list = Collection.objects.all()
    return render(request, "categories.html", {
        "category_list": category_list,
        "collections_list": collections_list,
    })


class FlowersListView(ListView):
    model = Flowers
    template_name = 'all_products.html'
    context_object_name = 'flowers_list'

class FlowersDetailView(DetailView):
    model = Flowers
    template_name = 'flowers/flowers_detail.html'
    context_object_name = 'flowers'

class FlowersCreateView(CreateView):
    model = Flowers
    form_class = FlowersForm
    template_name = 'flowers/flowers_form.html'
    success_url = reverse_lazy('all_products_view')

class FlowersUpdateView(UpdateView):
    model = Flowers
    form_class = FlowersForm
    template_name = 'flowers/flowers_form.html'
    success_url = reverse_lazy('all_products_view')

class FlowersDeleteView(DeleteView):
    model = Flowers
    template_name = 'flowers/flowers_confirm_delete.html'
    success_url = reverse_lazy('all_products_view')



class CategoryListView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'category_list'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/categories_detail.html'
    context_object_name = 'category'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/categories_form.html'
    success_url = reverse_lazy('categories_view')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/categories_form.html'
    success_url = reverse_lazy('categories_view')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'categories/categories_confirm_delete.html'
    success_url = reverse_lazy('categories_view')



class CollectionListView(ListView):
    model = Collection
    template_name = 'categories.html'
    context_object_name = 'collections_list'

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'collections/collections_detail.html'
    context_object_name = 'collection'

class CollectionCreateView(CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'collections/collections_form.html'
    success_url = reverse_lazy('categories_view')

class CollectionUpdateView(UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'collections/collections_form.html'
    success_url = reverse_lazy('categories_view')

class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'collections/collections_confirm_delete.html'
    success_url = reverse_lazy('categories_view')



class SupplierListView(ListView):
    model = Supplier
    template_name = 'suppliers/suppliers_list.html'
    context_object_name = 'suppliers_list'

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'suppliers/suppliers_detail.html'
    context_object_name = 'supplier'

class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/suppliers_form.html'
    success_url = reverse_lazy('suppliers_list')

class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/suppliers_form.html'
    success_url = reverse_lazy('suppliers_list')

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'suppliers/suppliers_confirm_delete.html'
    success_url = reverse_lazy('suppliers_list')



class PromoCodeListView(ListView):
    model = PromoCode
    template_name = 'promocodes/promocodes_list.html'
    context_object_name = 'promocodes_list'

class PromoCodeDetailView(DetailView):
    model = PromoCode
    template_name = 'promocodes/promocodes_detail.html'
    context_object_name = 'promocode'

class PromoCodeCreateView(CreateView):
    model = PromoCode
    form_class = PromoCodeForm
    template_name = 'promocodes/promocodes_form.html'
    success_url = reverse_lazy('promocodes_list')

class PromoCodeUpdateView(UpdateView):
    model = PromoCode
    form_class = PromoCodeForm
    template_name = 'promocodes/promocodes_form.html'
    success_url = reverse_lazy('promocodes_list')

class PromoCodeDeleteView(DeleteView):
    model = PromoCode
    template_name = 'promocodes/promocodes_confirm_delete.html'
    success_url = reverse_lazy('promocodes_list')


# Методы корзины 

def get_cart(request):
    return request.session.get('cart', {})

def set_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def get_applied_promo(request):
    return request.session.get('applied_promo')

def set_applied_promo(request, promo_data):
    request.session['applied_promo'] = promo_data
    request.session.modified = True

def clear_applied_promo(request):
    request.session.pop('applied_promo', None)

def add_to_cart(request, flower_id):
    cart = get_cart(request)
    flower_id_str = str(flower_id)
    cart[flower_id_str] = cart.get(flower_id_str, 0) + 1
    set_cart(request, cart)
    messages.success(request, 'Товар добавлен в корзину')
    return redirect(request.META.get('HTTP_REFERER', 'all_products_view'))

def remove_from_cart(request, flower_id):
    cart = get_cart(request)
    flower_id_str = str(flower_id)
    if flower_id_str in cart:
        del cart[flower_id_str]
        set_cart(request, cart)
        messages.success(request, 'Товар удалён из корзины')
    return redirect('cart_view')

def update_cart(request, flower_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = get_cart(request)
        flower_id_str = str(flower_id)
        if quantity > 0:
            cart[flower_id_str] = quantity
        else:
            cart.pop(flower_id_str, None)
        set_cart(request, cart)
        messages.success(request, 'Количество обновлено')
    return redirect('cart_view')

def cart_view(request):
    cart = get_cart(request)
    cart_items = []
    raw_total = 0

    for flower_id_str, quantity in cart.items():
        try:
            flower = Flowers.objects.get(pk=int(flower_id_str), is_exists=True)
        except Flowers.DoesNotExist:
            continue
        subtotal = flower.price * quantity
        raw_total += subtotal
        cart_items.append({
            'flower': flower,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    applied_promo = get_applied_promo(request)
    discount_percent = 0
    promo_code_str = None

    if request.method == 'POST' and 'apply_promo' in request.POST:
        code = request.POST.get('promo_code', '').strip()
        if code:
            try:
                promo = PromoCode.objects.get(code=code, is_active=True)
                now = timezone.now()
                if promo.valid_from <= now <= promo.valid_to:
                    applied_promo = {'code': promo.code, 'discount_percent': promo.discount_percent}
                    set_applied_promo(request, applied_promo)
                    messages.success(request, f'Промокод {promo.code} применён! Скидка {promo.discount_percent}%')
                else:
                    messages.error(request, 'Срок действия промокода истёк')
            except PromoCode.DoesNotExist:
                messages.error(request, 'Промокод не найден или неактивен')
        else:
            messages.error(request, 'Введите промокод')

    if applied_promo:
        discount_percent = applied_promo['discount_percent']
        promo_code_str = applied_promo['code']

    discount_amount = raw_total * discount_percent / 100
    total_price = raw_total - discount_amount

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'raw_total': raw_total,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'total_price': total_price,
        'promo_code_str': promo_code_str,
    })

def checkout(request):
    if request.method == 'POST':
        cart = get_cart(request)
        if not cart:
            messages.error(request, 'Корзина пуста')
            return redirect('cart_view')

        delivery_address = request.POST.get('delivery_address', '')
        comment = request.POST.get('comment', '')

        applied_promo = get_applied_promo(request)
        discount_percent = applied_promo['discount_percent'] if applied_promo else 0

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            status='new',
            total_price=0,
            delivery_address=delivery_address,
            comment=comment
        )

        total = 0
        for flower_id_str, quantity in cart.items():
            try:
                flower = Flowers.objects.get(pk=int(flower_id_str), is_exists=True)
            except Flowers.DoesNotExist:
                continue
            price = flower.price
            OrderItem.objects.create(
                order=order,
                flower=flower,
                quantity=quantity,
                price=price
            )
            total += price * quantity

        discount_amount = total * discount_percent / 100
        total -= discount_amount
        order.total_price = total
        order.save()

        request.session.pop('cart', None)
        clear_applied_promo(request)

        messages.success(request, f'Заказ №{order.id} успешно оформлен! Итоговая сумма: {total:.2f} руб.')
        return redirect('main_view')

    return redirect('cart_view')
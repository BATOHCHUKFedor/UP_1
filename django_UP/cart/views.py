from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from flower_shop.models import Flowers, OrderItem 
from .forms import CartAddProductForm, OrderForm
from .cart import Cart, get_applied_promo, set_applied_promo, clear_applied_promo
from flower_shop.models import PromoCode



def get_cart_context(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    raw_total = cart.get_total_price()

    applied_promo = get_applied_promo(request)
    discount_percent = 0
    promo_code_str = None

    if applied_promo:
        discount_percent = applied_promo['discount_percent']
        promo_code_str = applied_promo['code']

    discount_amount = raw_total * Decimal(discount_percent) / 100
    total_price = raw_total - discount_amount

    return {
        'cart_items': cart_items,
        'raw_total': raw_total,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'total_price': total_price,
        'promo_code_str': promo_code_str,
    }


def cart_detail(request):
    context = get_cart_context(request)

    if request.method == 'POST' and 'apply_promo' in request.POST:
        code = request.POST.get('promo_code', '').strip()
        if code:
            try:
                promo = PromoCode.objects.get(code=code, is_active=True)
                now = timezone.now()
                if promo.valid_from <= now <= promo.valid_to:
                    applied_promo = {
                        'code': promo.code,
                        'discount_percent': promo.discount_percent
                    }
                    set_applied_promo(request, applied_promo)
                    messages.success(request, f'Промокод {promo.code} применён! Скидка {promo.discount_percent}%')
                else:
                    messages.error(request, 'Срок действия промокода истёк')
            except PromoCode.DoesNotExist:
                messages.error(request, 'Промокод не найден или неактивен')
        else:
            messages.error(request, 'Введите промокод')
        context = get_cart_context(request)

    return render(request, 'cart/detail.html', context)

@require_POST
def cart_add(request, product_id):

    cart = Cart(request)
    product = get_object_or_404(Flowers, pk=product_id, is_exists=True)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        count = form.cleaned_data['count']
        update_count = form.cleaned_data['reload']
        cart.add(product, count, update_count)
        messages.success(request, 'Корзина обновлена')
    else:
        messages.error(request, 'Неверные данные')
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))


def cart_remove(request, product_id):

    cart = Cart(request)
    product = get_object_or_404(Flowers, pk=product_id)
    cart.remove(product)
    messages.success(request, 'Товар удалён из корзины')
    return redirect('cart:cart_detail')


def cart_clear(request):

    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Корзина очищена')
    return redirect('cart:cart_detail')

@login_required
def cart_buy(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'Корзина пуста')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            applied_promo = get_applied_promo(request)
            discount_percent = applied_promo['discount_percent'] if applied_promo else 0

            total_before_discount = cart.get_total_price()
            discount_amount = total_before_discount * Decimal(discount_percent) / 100
            total = total_before_discount - discount_amount

            order = form.save(commit=False)
            order.user = request.user
            order.status = 'new'
            order.total_price = total
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    flower=item['product'],
                    quantity=item['count'],
                    price=item['price']
                )

            cart.clear()
            clear_applied_promo(request)

            messages.success(request, f'Заказ №{order.pk} успешно оформлен! Сумма: {total:.2f} руб.')
            return redirect('main_view')
        else:
            context = get_cart_context(request)
            context['form_order'] = form   
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
            return render(request, 'cart/detail.html', context)
    else:
        return redirect('cart:cart_detail')
  
from decimal import Decimal
from django.conf import settings
from flower_shop.models import Flowers

class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Flowers.objects.filter(pk__in=product_ids, is_exists=True)
        for product in products:
            item = self.cart[str(product.pk)].copy()
            item['product'] = product
            item['total_price'] = Decimal(item['price']) * int(item['count'])
            yield item

    def __len__(self):
        return sum(int(item['count']) for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product, count=1, update_count=False):
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'count': 0,
                'price': str(product.price)
            }
        if update_count:
            self.cart[product_id]['count'] = count
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def remove(self, product):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        total = Decimal('0')
        for item in self.cart.values():
            total += Decimal(item['price']) * int(item['count'])
        return total

    def clear(self):
        self.session.pop(settings.CART_SESSION_ID, None)
        self.session.modified = True

    def get_items(self):
        items = []
        for item in self:
            items.append({
                'product': item['product'],
                'quantity': item['count'],
                'price': Decimal(item['price']),
                'subtotal': item['total_price'],
            })
        return items
    

def get_applied_promo(request):
    return request.session.get('applied_promo')

def set_applied_promo(request, promo_data):
    request.session['applied_promo'] = promo_data
    request.session.modified = True

def clear_applied_promo(request):
    request.session.pop('applied_promo', None)
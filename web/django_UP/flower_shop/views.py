from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import * 
from django.urls import reverse_lazy
from .forms import *
import random
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from cart.forms import CartAddProductForm

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

def categories_view(request):
    category_list = Category.objects.all()
    collections_list = Collection.objects.all()
    return render(request, "categories.html", {
        "category_list": category_list,
        "collections_list": collections_list,
    })

@login_required
def user_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})


class FlowersListView(ListView):
    model = Flowers
    template_name = 'all_products.html'
    context_object_name = 'flowers_list'

class FlowersDetailView(DetailView):
    model = Flowers
    template_name = 'flowers/flowers_detail.html'
    context_object_name = 'flowers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_cart'] = CartAddProductForm()
        return context

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


@method_decorator(permission_required('flower_shop.view_supplier'), name='dispatch')
class SupplierListView(ListView):
    model = Supplier
    template_name = 'suppliers/suppliers_list.html'
    context_object_name = 'suppliers_list'

@method_decorator(permission_required('flower_shop.view_supplier'), name='dispatch')
class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'suppliers/suppliers_detail.html'
    context_object_name = 'supplier'

@method_decorator(permission_required('flower_shop.add_supplier'), name='dispatch')
class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/suppliers_form.html'
    success_url = reverse_lazy('suppliers_list')

@method_decorator(permission_required('flower_shop.change_supplier'), name='dispatch')
class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/suppliers_form.html'
    success_url = reverse_lazy('suppliers_list')

@method_decorator(permission_required('flower_shop.delete_supplier'), name='dispatch')
class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'suppliers/suppliers_confirm_delete.html'
    success_url = reverse_lazy('suppliers_list')



@method_decorator(permission_required('flower_shop.view_promocode'), name='dispatch')
class PromoCodeListView(ListView):
    model = PromoCode
    template_name = 'promocodes/promocodes_list.html'
    context_object_name = 'promocodes_list'

@method_decorator(permission_required('flower_shop.view_promocode'), name='dispatch')
class PromoCodeDetailView(DetailView):
    model = PromoCode
    template_name = 'promocodes/promocodes_detail.html'
    context_object_name = 'promocode'

@method_decorator(permission_required('flower_shop.add_promocode'), name='dispatch')
class PromoCodeCreateView(CreateView):
    model = PromoCode
    form_class = PromoCodeForm
    template_name = 'promocodes/promocodes_form.html'
    success_url = reverse_lazy('promocodes_list')

@method_decorator(permission_required('flower_shop.change_promocode'), name='dispatch')
class PromoCodeUpdateView(UpdateView):
    model = PromoCode
    form_class = PromoCodeForm
    template_name = 'promocodes/promocodes_form.html'
    success_url = reverse_lazy('promocodes_list')

@method_decorator(permission_required('flower_shop.delete_promocode'), name='dispatch')
class PromoCodeDeleteView(DeleteView):
    model = PromoCode
    template_name = 'promocodes/promocodes_confirm_delete.html'
    success_url = reverse_lazy('promocodes_list')

#Аутентификация
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('main_view')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'auth/login.html', context)

def registration_user(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            login(request, form.save())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('main_view')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'auth/registration.html', context)

def logout_user(request):
    logout(request)
    return redirect('main_view')

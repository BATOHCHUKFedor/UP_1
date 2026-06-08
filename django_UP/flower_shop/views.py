from django.shortcuts import render

def main_view(request):
    return render(request, "main.html")

def info_view(request):
    return render(request, "info.html")

def contacts_view(request):
    return render(request, "contacts.html")

def our_whereabouts_view(request):
    return render(request, "our_whereabouts.html")

def products_view(request):
    return render(request, "products.html")

def categories_view(request):
    return render(request, "categories.html")

def all_products_view(request):
    return render(request, "all_products.html")

def cart_view(request):
    return render(request, "cart.html")
from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.

def home(request):
    products = Product.objects.all()[:8]
    brands = Brand.objects.all()[:8]
    return render(request, "Store/home.html", {
        "product": products,
        "brand": brands
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, "Store/product_list.html", {
        "product":  products
    })

def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "Store/product_description.html", {
        "product": product
    })
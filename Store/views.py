from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.

def home(request):
    brands = Brand.objects.all()[:8]
    categories = Category.objects.all()

    category_menu = []

    for category in categories:
        category_brands = Brand.objects.filter(product_category=category).distinct()

        category_menu.append({
            "category": category,
            "brands": category_brands
        })

    collections = []

    for category in categories:
        product = Product.objects.filter(category=category).first()

        if product:
            collections.append({
                "category": category,
                "product": product
            })

    return render(request, "Store/home.html", {
        "categories": categories,
        "brands": brands,
        "collections": collections,
        "category_menu": category_menu
    })

def product_list(request):
    category_menu = []

    for category in Category.objects.all():
        brands = Brand.objects.filter(product_category=category).distinct()

        category_menu.append({
            "category": category,
            "brands": brands
        })

    products = Product.objects.all()

    return render(request, "Store/product_list.html", {
        "products":  products,
        "category_menu": category_menu 
    })

def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "Store/product_description.html", {
        "product": product
    })
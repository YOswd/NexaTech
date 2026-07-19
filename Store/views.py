from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import login
from .models import *

# Create your views here.

def home(request):
    brands = Brand.objects.all()[:8]
    categories = Category.objects.all()

    category_menu = []

    for category in categories:

        category_brands = Brand.objects.filter(product__category=category)

        category_menu.append({
            "category": category,
            "brands": category_brands
        })

    collections = []

    for category in categories:

        product = Product.objects.filter(
            category=category
        ).first()

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
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    category = request.GET.get("category")
    brand = request.GET.get("brand")
    search = request.GET.get("search")

    if category:
        products = products.filter(category_id=category)
    
    if brand:
        products = products.filter(brand_id=brand)
    
    if search:
        products = products.filter(product_name_icontains=search)

    return render(request, "Store/product_list.html", {
        "products":  products,
        "categories": categories,
        "brands": brands 
    })

from django.db import connection


def product_details(request, id):
    product = Product.objects.get(id=id)

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT average_rating(%s)
            FROM dual
            """,
            [id]
        )

        average = cursor.fetchone()[0]


    return render(request, "Store/product_details.html", {
            "product": product,
            "average_rating": average
        })

def category_products(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)

    return render(request, "Store/category_products.html", {
        "category": category,
        "products": products
    })

def brand_products(request, id):
    brand = get_object_or_404(Brand, id=id)
    products = Product.objects.filter(brand=brand)

    return render(request, "Store/brand_products.html", {
        "brand": brand,
        "products": products
    })

def add_to_cart(request, product_id):
    user = User.objects.first()
    cart = Cart.objects.filter(user=user).first()

    if cart is None:
        cart = Cart.objects.create(user=user)

    product = get_object_or_404(Product,id=product_id)

    item = CartItem.objects.filter(
        cart=cart,
        product=product
    ).first()

    if item:
        item.quantity += 1
        item.save()

    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )

    return redirect("cart")

def cart(request):
    user = User.objects.first()
    cart = Cart.objects.filter(user=user).first()

    items = []
    total = 0

    if cart:
        items = CartItem.objects.filter(cart=cart)

        for item in items:
            total += item.product.price * item.quantity

    return render(request, "Store/cart.html", {
        "items": items,
        "total": total
    })

@login_required
def checkout(request):

    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        return redirect("cart")

    items = CartItem.objects.filter(cart=cart)

    if not items.exists():
        return redirect("cart")

    total = 0

    for item in items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
        user=request.user,
        amount=total,
        status="Pending"
    )

    for item in items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        item.product.stock_quantity -= item.quantity
        item.product.save()

    items.delete()

    return redirect("order_success", order.id)

def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():

            return render(request, "Store/register.html", {
                "error": "Username already exists."
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("home")

    return render(request, "Store/register.html")

@login_required
def add_review(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":
        rating = request.POST["rating"]
        comment = request.POST["comment"]

        Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            comment=comment,
            date=timezone.now()
        )

        return redirect(
            "product_details",
            id=product.id
        )

    return redirect(
        "product_details",
        id=product.id
    )

@login_required
def order_success(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "Store/order_success.html",
        {
            "order": order
        }
    )
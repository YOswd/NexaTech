from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("product/<int:id>/", views.product_details, name="product_details"),
    path("category/<int:id>/", views.category_products, name="category_products"),
    path("brand/<int:id>/", views.brand_products, name="brand_products"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("login/", auth_views.LoginView.as_view(template_name="Store/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views.register, name="register"),
    path("product/<int:product_id>/review/", views.add_review, name="add_review"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
]
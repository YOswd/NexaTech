from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.category_name
    
class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.brand_name
    
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.supplier_name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.IntegerField()
    stock_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    
class SpecificationTemplate(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    specification_name = models.CharField(max_length=100)

    def __str__(self):
        return self.specification_name
    
class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    template = models.ForeignKey(SpecificationTemplate, on_delete=models.CASCADE)
    specification_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.product_name}"

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.supplier.supplier_name}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.product_name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.product_name}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.product_name}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username}"
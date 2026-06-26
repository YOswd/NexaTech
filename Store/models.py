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
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.category_name
    
class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.brand_name
    
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    
class Product(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.IntegerField()
    stock_quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    
class SpecificationTemplate(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    specification_name = models.CharField(max_length=100)

    def __str__(self):
        return self.specification_name
    
class ProductSpecification(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    template_id = models.ForeignKey(SpecificationTemplate, on_delete=models.CASCADE)
    specification_value = models.CharField(max_length=255)

    def __str__(self):
        return self.specification_value

class Purchase(models.Model):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()

    def __str__(self):
        return self.amount

class PurchaseItems(models.Model):
    purchase_id = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost = models.IntegerField()

    def __str__(self):
        return self.quantity

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.TimeField()

    def __str__(self):
        return self.created_at

class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.quantity
    
class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status
    
class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.quantity
    
class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.comment
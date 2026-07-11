from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(SpecificationTemplate)
admin.site.register(ProductSpecification)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(UserProfile)
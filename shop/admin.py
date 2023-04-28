from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Order)
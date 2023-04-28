from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
class User(AbstractUser):
    is_public =models.BooleanField(default=False)
    is_private =models.BooleanField(default=False)
    profile_Picture=models.ImageField(upload_to="photo/" ,null=True,blank=True)

class Category(models.Model):
    cat_title=models.CharField(max_length=150)
    cat_description=models.TextField(null=True)
    slug=models.SlugField()
    def __str__(self):
        return self.cat_title

class Product(models.Model):    
    p_name=models.CharField(max_length=150)
    p_category=models.ForeignKey(Category,on_delete=models.CASCADE)
    slug=models.SlugField()
    p_description=models.TextField()
    p_image=models.ImageField()
    p_price=models.IntegerField()
    p_discount_price=models.FloatField(null=True,blank=True)
    p_brand=models.CharField(max_length=150)
    def __str__(self):
        return self.p_name
    def getSaveingPercentage(self):
        result = ((self.p_price - self.p_discount_price) / self.p_price)*100
        return f"%.2f"% result
class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    item=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    def __str__(self):
        return self.item.p_name
    
    def get_discount_price(self):
        return self.item.p_discount_price * self.qty
    
    def get_price(self):
        return self.item.p_price * self.qty
    def get_final_amount(self):
        if self.item.p_discount_price:
            return self.get_discount_price()
        else:
            return self.get_price()
class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    items=models.ManyToManyField(OrderItem)
    created_at=models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey("Coupon",on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.user.username
    def get_total_amount(self):
        total = 0 
        for oi in self.item.all():
            total+=oi.get_final_amount()
        if self.coupon:
            total -= self.coupon.amount
        return total
    def get_price_amount(self):
        total=0
        for oi in self.items.all():
            total += oi.get_price()
        return total
    def get_tax_amount(self):
        return (self.get_total_amount() * 0.18)
    def get_payment_amount(self):
        return self.get_total_amount() + self.get_tax_amount()
    def get_discount_amount(self):
        return self.get_price_amount() - self.get_total_amount()
class Coupon(models.Model):
    code=models.CharField(max_length=20)
    amount=models.FloatField()
    def __str__(self):
        return self.code
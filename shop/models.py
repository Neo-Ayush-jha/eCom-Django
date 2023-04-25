from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_public =models.BooleanField(default=False)
    is_private =models.BooleanField(default=False)

class Category(models.Model):
    cat_title=models.CharField(max_length=150)
    cat_description=models.TextField(null=True)
    slug=models.SlugField()
    def __str__(self):
        return self.cat_title

class Product(models.Model):    
    p_name=models.CharField(max_length=150)
    p_category=models.ForeignKey(Category,on_delete=models.CASCADE)
    p_slug=models.SlugField()
    p_description=models.TextField()
    p_image=models.ImageField()
    p_price=models.IntegerField()
    p_discount_price=models.FloatField(null=True,blank=True)
    p_brand=models.CharField(max_length=150)
    def __str__(self):
        return self.p_name
    def getSaveingPercentage(self):
        result = ((self.p_price-self.p_discount_price)/self.p_price)*100
        return f"%.2f"% result
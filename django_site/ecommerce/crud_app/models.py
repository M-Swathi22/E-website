from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/',null=True,blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Create your models here.

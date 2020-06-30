from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    CATEGORY = (
        ('1','New'),
        ('2','Impulsive'),
        ('3','Discount'),
        ('4','Loyal'),
    )
    category =models.CharField(choices=CATEGORY, max_length=50, null=True, default=CATEGORY[0][1])
    profile_pic = models.ImageField( upload_to='profile_pics', default='default.jpg',null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    # def __str__(self):
    #     return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    display_picture = models.ImageField(upload_to='product_images', default='default_product.jpg', null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    offer = models.FloatField(null=True, blank=True)
    CATEGORY = (
        ('Indoor','Indoor'),
        ('Out Door','Out Door'),
    )
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    description = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    offer_added = models.DateTimeField(auto_now=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    STATUS = (
        ('Pending','Pending'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


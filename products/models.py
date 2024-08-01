
from django.db import models

# Create your models here.

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)


    def __str__(self):
       return self.name


    def __get_friendly_name(self):
        return self.friendly_name

class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sizes = models.CharField(max_length=254, null=True, blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20,default='Unknown')
    country = models.CharField(max_length=40, default= 'USA')
    postcode = models.CharField(max_length=20, blank=True, null=True)
    town_or_city = models.CharField(max_length=40,default='Unknown')
    street_address1 = models.CharField(max_length=80,default='Unknown')
    street_address2 = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    review_text = models.TextField(null =True, blank=True)
    
    def __str__(self):
        return f"Review by {self.customer.full_name()} for {self.product.name}"

    

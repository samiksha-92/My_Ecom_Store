from django.db import models

# Create your models here.

from products.models import Customer
from products.models import Product
from django.db.models import Sum
from django.conf import settings

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=32, editable=False, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    first_name = models.CharField(max_length=50, default='Unknown')
    last_name = models.CharField(max_length=50, default='NA')
    email = models.EmailField(default='example@example.com')
    phone_number = models.CharField(max_length=20, default='0000000000')
    country = models.CharField(max_length=40, default='Unknown Country')
    postcode = models.CharField(max_length=20, default='000000')
    town_or_city = models.CharField(max_length=40, default='Unknown City')
    street_address1 = models.CharField(max_length=80, default='Unknown Address')
    street_address2 = models.CharField(max_length=80, blank=True, null=True)
    county = models.CharField(max_length=80, blank=True, null=True)


    def _generate_order_number(self):
        """ Generate a unique order number """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """ Update grand total each time a line item is added, accounting for delivery costs. """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """ Override save method to set order number if not already set. """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} by {self.customer.full_name()}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
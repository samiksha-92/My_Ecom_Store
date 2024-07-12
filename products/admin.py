from django.contrib import admin
from .models import Product,Category,Customer,Review

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer','review_text')
    search_fields = ('customer__first_name', 'customer__last_name', 'product__name')    


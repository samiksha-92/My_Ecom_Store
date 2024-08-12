from django.contrib import admin
from .models import Product,Category,Customer,Review

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )    

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number',)
    search_fields = ('first_name', 'last_name', 'email',)

  


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'get_user_full_name','review_text')

    def get_user_full_name(self, obj):
        return obj.profile.user.get_full_name()

    get_user_full_name.short_description = 'User' 

    


from django.contrib import admin

# Register your models here.

from .models import Order, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    extra = 0  # Prevents Django from adding empty fields by default

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date', 'delivery_cost', 'order_total', 'grand_total','original_bag', 'stripe_pid',)

    fields = ('customer', 'order_number','profile', 'date', 'delivery_cost', 'order_total', 'grand_total','original_bag', 'stripe_pid',)

    list_display = ('order_number', 'customer', 'date', 'order_total', 'delivery_cost', 'grand_total', 'profile',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)

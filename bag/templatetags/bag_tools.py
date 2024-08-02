from django import template

register  = template.Library()

@register.filter
def cal_subtotal(price,quantity):
    return price*quantity
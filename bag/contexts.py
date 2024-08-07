from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product







def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for product_id_str, quantity in bag.items():
        try:
            product_id = int(product_id_str)
        except ValueError:
            # Log or print error if product_id_str is not an integer
            continue  # Skip this entry if there's a format error
        
        product = get_object_or_404(Product, pk=product_id)

        # Ensure quantity is an integer
        if isinstance(quantity, int):
            # Calculate subtotal
            subtotal = quantity * product.price
            total += subtotal
            product_count += quantity

            bag_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'product': product,
                'subtotal': subtotal  
            })
        else:
            print(f"Unexpected quantity type for {product_id_str}: {type(quantity)}")

    # Calculate delivery and grand total
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context

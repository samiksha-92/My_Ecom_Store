from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for product_key, item_data in bag.items():
        try:
            # Split the product_key into product_id and size
            product_id_str, size = product_key.split('_', 1)
            product_id = int(product_id_str)
        except (ValueError, IndexError):
            # Log or print error if product_key is not in expected format
            continue  # Skip this entry if there's a format error
        
        product = get_object_or_404(Product, pk=product_id)

        # Ensure item_data is a dictionary
        if isinstance(item_data, dict):
            quantity = item_data.get('quantity', 0)  # Use .get() to avoid KeyError
            if isinstance(quantity, int):
                # Calculate subtotal
                subtotal = quantity * product.price
                total += subtotal
                product_count += quantity

                # Add item details to the bag_items list
                bag_items.append({
                    'product_id': product_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                    'subtotal': subtotal  # Include subtotal in bag_items
                })
            else:
                print(f"Unexpected quantity type for {product_key}: {type(quantity)}")
        else:
            print(f"Unexpected item_data type for {product_key}: {type(item_data)}")

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

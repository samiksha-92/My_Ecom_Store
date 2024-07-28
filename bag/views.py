from django.shortcuts import render,redirect, get_object_or_404

from products.models import Product

# Create your views here.

def view_bag(request):
    return render (request, 'bag/bag.html')


from django.shortcuts import get_object_or_404
from products.models import Product

def add_to_bag(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity_str = request.POST.get('quantity','0')

    try:
        # Convert quantity to int, default to 1 if conversion fails
        quantity = int(quantity_str)
    except ValueError:
        quantity = 1  



    size = request.POST.get('size', None)
    bag = request.session.get('bag', {})

    # Create a unique key for each product and size combination
    product_key = f"{product_id}_{size}"

    # Debug print to check the current state of the bag
    print("Current Bag State:", bag)
    print("Product Key:", product_key)
    
    if product_key in bag:
        if isinstance(bag[product_key], dict):
            # Increment quantity if product already in bag
            bag[product_key]['quantity'] += quantity
        else:
            print(f"Unexpected item data type for {product_key}: {type(bag[product_key])}")
            bag[product_key] = {'quantity': quantity, 'size': size}
    else:
        # Add product with quantity and size to the bag
        bag[product_key] = {'quantity': quantity, 'size': size}

    # Save the updated bag to the session
    request.session['bag'] = bag
    
    return redirect(request.POST.get('redirect_url', 'products'))


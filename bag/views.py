from django.shortcuts import render,redirect, get_object_or_404
from .contexts import bag_contents
from django.http import JsonResponse

from products.models import Product

# Create your views here.

def view_bag(request):
    return render (request, 'bag/bag.html')



def add_to_bag(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity_str = request.POST.get('quantity', '0')

    try:
        quantity = int(quantity_str)
    except ValueError:
        quantity = 1

    size = request.POST.get('size', None)
    bag = request.session.get('bag', {})

    product_key = f"{product_id}_{size}"

    # Debug print to check the current state of the bag
    print("Current Bag State:", bag)
    print("Product Key:", product_key)

    if product_key in bag:
        if isinstance(bag[product_key], dict):
            bag[product_key]['quantity'] += quantity
        else:
            print(f"Unexpected item data type for {product_key}: {type(bag[product_key])}")
            bag[product_key] = {'quantity': quantity, 'size': size}
    else:
        bag[product_key] = {'quantity': quantity, 'size': size}

    request.session['bag'] = bag
    return redirect(request.POST.get('redirect_url', 'products'))



def update_bag(request):
    if request.method == 'POST':
        product_key = request.POST.get('product_key')
        new_quantity = int(request.POST.get('quantity', 1))

        bag = request.session.get('bag', {})
        if product_key in bag:
            if isinstance(bag[product_key], dict):
                if new_quantity > 0:
                    bag[product_key]['quantity'] = new_quantity
                else:
                    del bag[product_key]
            else:
                print(f"Unexpected item data type for {product_key}: {type(bag[product_key])}")
                bag[product_key] = {'quantity': new_quantity, 'size': None}

            request.session['bag'] = bag

        context = bag_contents(request)

        return JsonResponse({
            'status': 'success',
            'total': float(context['total']),
            'grand_total': float(context['grand_total']),
            'subtotal': next((item['subtotal'] for item in context['bag_items'] if f"{item['product_id']}_{item['size']}" == product_key), 0)
        })
    return JsonResponse({'status': 'failed'})



            





def remove_from_bag(request):
    if request.method == 'POST':
        product_key = request.POST.get('product_key')
        bag = request.session.get('bag', {})

        if product_key in bag:
            del bag[product_key]
            request.session['bag'] = bag

        context = bag_contents(request)

        return JsonResponse({
            'status': 'success',
            'total': context['total'],
            'grand_total': context['grand_total'],
        })
    return JsonResponse({'status': 'failed'})

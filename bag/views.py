from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .contexts import bag_contents
from django.http import JsonResponse

from products.models import Product




def view_bag(request):
    return render(request, 'bag/bag.html')

def add_to_bag(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity_str = request.POST.get('quantity', '0')

    try:
        quantity = int(quantity_str)
    except ValueError:
        quantity = 1


    bag = request.session.get('bag', {})
    # Use product_id directly as the key
    if str(product_id) in bag:
        bag[str(product_id)] += quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[str(product_id)]}')
    else:
        bag[str(product_id)] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(request.POST.get('redirect_url', 'products'))

def update_bag(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_quantity = int(request.POST.get('quantity', 1))

        bag = request.session.get('bag', {})
        if product_id in bag:
            if new_quantity > 0:
                bag[product_id] = new_quantity
                messages.success(request, f'Updated product quantity to {new_quantity}')
            else:
                del bag[product_id]
                messages.success(request, 'Removed product from your bag')

            request.session['bag'] = bag

        context = bag_contents(request)

        return JsonResponse({
            'status': 'success',
            'total': float(context['total']),
            'grand_total': float(context['grand_total']),
            'subtotal': next((item['subtotal'] for item in context['bag_items'] if str(item['product_id']) == product_id), 0)
        })
    return JsonResponse({'status': 'failed'})
      


        
        
def remove_from_bag(request):
    if request.method == 'POST':
        product_id= request.POST.get('product_id')
        bag = request.session.get('bag', {})

        if product_id in bag:
            del bag[product_id]
            request.session['bag'] = bag
            messages.success(request, 'Removed product from your bag')

        context = bag_contents(request)

        return JsonResponse({
            'status': 'success',
            'total': context['total'],
            'grand_total': context['grand_total'],
        })
    return JsonResponse({'status': 'failed'})









            






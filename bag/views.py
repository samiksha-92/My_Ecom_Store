from django.shortcuts import render,redirect, get_object_or_404

from products.models import Product

# Create your views here.

def view_bag(request):
    return render (request, 'bag/bag.html')

def add_to_bag(request,product_id):

    product = get_object_or_404(Product, pk = product_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('size',None)
    bag = request.session.get('bag',{})

    product_id = int(product_id)

    product_key = f"{product_id}_{size}"

    if product_key in bag:
        bag[product_key]['quantity'] += quantity
    else:
        bag[product_key] = {'quantity' : quantity, 'size': size,}


    request.session['bag'] = bag
    
    
    return redirect(request.POST.get('redirect_url', 'products'))


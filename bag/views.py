from django.shortcuts import render,redirect, get_object_or_404

from products.models import Product

# Create your views here.

def view_bag(request):
    return render (request, 'bag/bag.html')

def add_to_bag(request,product_id):

    product = get_object_or_404(Product, pk = product_id)
    bag = request.session.get('bag',{})
    quantity = int(request.POST.get('quantity'))

    product_id = int(product_id)

    if product_id in bag:
        bag[product_id] += quantity
    else:
        bag[product_id] = quantity

    request.session['bag'] = bag
    print({k: v for k, v in bag.items() if k != 'product_id'})
    #print(request.session['bag'])

    return redirect(request.POST.get('redirect_url', 'products'))


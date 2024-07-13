from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
# Create your views here.

def all_products(request):

     query = request.GET.get('q')

     if query is None or query.strip() == '':
        return redirect('products')

     products = Product.objects.all()

     if query:
        products = products.filter(name__icontains=query)

     context = {
        'products': products,
    }

     return render(request, 'products/products.html', context)

def product_detail(request,pk):

    product = get_object_or_404(Product,pk=pk)
    context = {
        'product' : product,
    }
    
    return render (request, 'products/product_detail.html',context)    
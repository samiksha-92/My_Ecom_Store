from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib import messages
from .models import Product

# Create your views here.

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Product

def all_products(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
        if not products.exists():
            messages.error(request, "No products found matching your search criteria.")
    else:
        products = Product.objects.all()
        if request.GET.get('q') == '':
            messages.error(request, "Please enter a search term! currently it is empty")

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
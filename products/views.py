from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib import messages
from .models import Product

# Create your views here.

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product,Category



def all_products(request):
    
    products = Product.objects.all()

    # Initialize variables
    query = request.GET.get('q')
    categories = request.GET.getlist('category', None)

    
    if categories:
        products = products.filter(category__name__in=categories)
        categories = Category.objects.filter(name__in=categories)
    
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if not products.exists():
            messages.error(request, "No products found matching your search criteria.")
    
    # Handle empty search query
    if not query and request.GET.get('q') == '':
        messages.error(request, "Please enter a search term!")

    context = {
        'products': products,
        'current_categories': categories,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


     


        



def product_detail(request,pk):

    product = get_object_or_404(Product,pk=pk)
    context = {
        'product' : product,
    }
    
    return render (request, 'products/product_detail.html',context)    
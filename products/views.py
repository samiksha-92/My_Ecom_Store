from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import Product,Category
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm

    
    

def all_products(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    categories = request.GET.getlist('category')
    sort_by = request.GET.get('sort_by',None)


    # Handle category filtering
    if categories:
        # Check if categories contain a single comma-separated string
        if len(categories) == 1:
            categories = categories[0].split(',')
        products = products.filter(category__name__in=categories)
        selected_categories = Category.objects.filter(name__in=categories)
    else:
        selected_categories = None

    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if not products.exists():
            messages.error(request, "No products found matching your search criteria.")
        
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating_desc':
        products = products.order_by('-rating')

    if query is not None and query == '':
        messages.error(request, "Please enter a search term!")

    context = {
        'products': products,
        'current_categories': selected_categories,
        'search_term': query,
        'sort_by' : sort_by,
    }

    return render(request, 'products/products.html', context)
     



def product_detail(request,pk):

    product = get_object_or_404(Product,pk=pk)
    context = {
        'product' : product,
    }
    
    return render (request, 'products/product_detail.html',context)    





@user_passes_test(lambda u: u.is_superuser)
def product_management(request):
    products = Product.objects.all()
    return render(request, 'products/product_management.html', {'products': products})

@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_management')
        
    else:
        form = ProductForm()
        messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    
    
    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)



@user_passes_test(lambda u: u.is_superuser)
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_management')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/update_product.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_management')

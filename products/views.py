from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import Product,Category,Review,Customer
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm, ReviewForm
from django.contrib.auth.decorators import login_required
from profiles.models import Profile



    
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
    reviews = Review.objects.filter(product=product)
    review_form = ReviewForm()
    context = {
        'product' : product,
        'reviews': reviews,
        'review_form': review_form,
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





@login_required
def create_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    profile = request.user.profile  # Assume the user has a profile
    
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            if not review_form.cleaned_data.get('review_text').strip():
                messages.error(request, 'Review text cannot be empty.')
                return redirect('product_detail', pk=product.id)

            review = review_form.save(commit=False)
            review.product = product
            review.profile = profile  # Associate the review with the user's profile
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('product_detail', pk=product.id)
        else:
            messages.error(request, 'There was an error with your review. Please make sure to post something.')
    
    return redirect('product_detail', pk=product.id)

@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.profile != request.user.profile:
        messages.error(request, 'You are not authorized to edit this review.')
        return redirect('product_detail', pk=review.product.id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            messages.success(request, 'Your review has been updated.')
            return redirect('product_detail', pk=review.product.id)
        else:
            messages.error(request, 'There was an error with your review. Please try again.')

    else:
        review_form = ReviewForm(instance=review)

    context = {
        'review_form': review_form,
        'product': review.product
    }
    return render(request, 'products/update_review.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.profile != request.user.profile:
        messages.error(request, 'You are not authorized to delete this review.')
        return redirect('product_detail', pk=review.product.id)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('product_detail', pk=review.product.id)

    context = {
        'review': review
    }
    return render(request, 'products/delete_review.html', context)

# profiles/views.py

from django.shortcuts import render, redirect,get_object_or_404
from .forms import ProfileForm
from django.contrib import messages
from checkout.models import Order

def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    orders = profile.orders.all()

    context = {
        'form': form,
        'orders': orders,
    }
    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    context = {
        'order': order,
        
    }
    return render(request, 'profiles/order_history.html', context)
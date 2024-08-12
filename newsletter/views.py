# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterSubscriptionForm
from .models import NewsletterSubscription

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed to our newsletter!')
            return redirect('home')  # Redirect to home page or any other page
        else:
            messages.error(request, 'There was an error with your subscription. Please try again.')
    else:
        form = NewsletterSubscriptionForm()

    context = {
        'form': form,
    }
    return render(request, 'newsletter/subscribe_newsletter.html', context)

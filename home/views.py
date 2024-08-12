
from django.shortcuts import render, redirect
from django.contrib import messages
from newsletter.forms import NewsletterSubscriptionForm

def index(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            response = redirect('home')
            response.set_cookie('newsletter_subscribed', 'true', max_age=365*24*60*60)  # 1 year
            messages.success(request, 'You have successfully subscribed to the newsletter.')
            return response
    else:
        form = NewsletterSubscriptionForm()

    context = {
        'form': form,
    }
    return render(request, 'home/index.html', context)

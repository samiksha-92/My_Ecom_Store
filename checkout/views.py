from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from products.models import Customer  # Import Customer

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag")
        return redirect(reverse('products'))

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            
            # Extract form data
            first_name = order_form.cleaned_data.get('first_name')
            last_name = order_form.cleaned_data.get('last_name')
            email = order_form.cleaned_data.get('email')
            phone_number = order_form.cleaned_data.get('phone_number')
            country = order_form.cleaned_data.get('country')
            postcode = order_form.cleaned_data.get('postcode')
            town_or_city = order_form.cleaned_data.get('town_or_city')
            street_address1 = order_form.cleaned_data.get('street_address1')
            street_address2 = order_form.cleaned_data.get('street_address2')
            county = order_form.cleaned_data.get('county')

            customer, created = Customer.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number,
                    'country': country,
                    'postcode': postcode,
                    'town_or_city': town_or_city,
                    'street_address1': street_address1,
                    'street_address2': street_address2,
                    'county': county,
                }
            )

            if not created:
                customer.first_name = first_name
                customer.last_name = last_name
                customer.phone_number = phone_number
                customer.country = country
                customer.postcode = postcode
                customer.town_or_city = town_or_city
                customer.street_address1 = street_address1
                customer.street_address2 = street_address2
                customer.county = county
                customer.save()

            order.customer = customer
            order.save()

            messages.success(request, f"Order {order.order_number} placed successfully!")
            return redirect('order_confirmation', order_number=order.order_number)
        else:
            messages.error(request, "There was an error with your form. Please double-check your information.")
    else:
        order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        
    }
    return render(request, template, context)

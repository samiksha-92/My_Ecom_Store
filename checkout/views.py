from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Customer,Product
from bag.contexts import bag_contents
import stripe
from django.conf import settings



# Set the Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        # Debug: Print the bag to check its contents
        print("Bag contents:", bag)

        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            # Removed 'county' field as it's not part of the Customer model
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            
            # Create or update customer
            customer, created = Customer.objects.get_or_create(
                email=form_data['email'],
                defaults={
                    'first_name': form_data['first_name'],
                    'last_name': form_data['last_name'],
                    'phone_number': form_data['phone_number'],
                    'country': form_data['country'],
                    'postcode': form_data['postcode'],
                    'town_or_city': form_data['town_or_city'],
                    'street_address1': form_data['street_address1'],
                    'street_address2': form_data['street_address2'],
                }
            )
            if not created:
                customer.first_name = form_data['first_name']
                customer.last_name = form_data['last_name']
                customer.phone_number = form_data['phone_number']
                customer.country = form_data['country']
                customer.postcode = form_data['postcode']
                customer.town_or_city = form_data['town_or_city']
                customer.street_address1 = form_data['street_address1']
                customer.street_address2 = form_data['street_address2']
                customer.save()

            order.customer = customer
            order.save()

            for item_id, item_data in bag.items():
                try:
                    # Debug: Print the item_id to verify it's correct
                    print("Item ID:", item_id)

                    product = Product.objects.get(id=int(item_id))
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except ValueError:
                    print(f"Invalid product ID: {item_id}")
                    messages.error(request, (
                        "There was an error with one of the products in your bag. "
                        "Please call us for assistance!"
                    ))
                    order.delete()
                    return redirect(reverse('view_bag'))
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('order_confirmation', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

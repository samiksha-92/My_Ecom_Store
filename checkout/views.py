from django.shortcuts import render, redirect, reverse,get_object_or_404,HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Customer,Product
from bag.contexts import bag_contents
import stripe
from django.conf import settings
import json



@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.username,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


# Set the Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

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
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)

            customer_queryset = Customer.objects.filter(email=form_data['email'])
            if customer_queryset.exists():
                customer = customer_queryset.first()
                customer.first_name = form_data['first_name']
                customer.last_name = form_data['last_name']
                customer.phone_number = form_data['phone_number']
                customer.country = form_data['country']
                customer.postcode = form_data['postcode']
                customer.town_or_city = form_data['town_or_city']
                customer.street_address1 = form_data['street_address1']
                customer.street_address2 = form_data['street_address2']
                customer.save()
            else:
                customer = Customer.objects.create(
                    email=form_data['email'],
                    first_name=form_data['first_name'],
                    last_name=form_data['last_name'],
                    phone_number=form_data['phone_number'],
                    country=form_data['country'],
                    postcode=form_data['postcode'],
                    town_or_city=form_data['town_or_city'],
                    street_address1=form_data['street_address1'],
                    street_address2=form_data['street_address2'],
                )

            order.customer = customer
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in bag.items():
                try:
                    item_id = int(item_id)
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
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

            # Include the metadata
            intent = stripe.PaymentIntent.create(
                amount=int(order.get_total() * 100),
                currency=settings.STRIPE_CURRENCY,
                metadata={
                    'order_id': order.order_number,
                    'customer_id': customer.id,
                    'email': customer.email,
                }
            )


            return redirect(reverse('checkout_success', args=[order.order_number]))
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
            metadata={
                'bag': json.dumps(bag),
                'save_info': 'save-info' in request.POST,
                'username': request.user.username,
            }
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

def checkout_success(request, order_number):
    
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
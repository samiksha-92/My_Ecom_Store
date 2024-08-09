from django import forms
from .models import Order
from products.models import Customer  
from django_countries.fields import CountryField


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name *',
            'class': 'stripe-style-input',
            'autofocus': True
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name *',
            'class': 'stripe-style-input',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email Address *',
            'class': 'stripe-style-input',
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone Number *',
            'class': 'stripe-style-input',
        })
    )
    country = CountryField().formfield(
        widget=forms.Select(attrs=
        {'placeholder': 'Country *',
        'class': 'stripe-style-input'})
    )
    postcode = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Postal Code *',
            'class': 'stripe-style-input',
        })
    )
    town_or_city = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Town or City *',
            'class': 'stripe-style-input',
        })
    )
    street_address1 = forms.CharField(
        max_length=80,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Street Address 1 *',
            'class': 'stripe-style-input',
        })
    )
    street_address2 = forms.CharField(
        max_length=80,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Street Address 2',
            'class': 'stripe-style-input',
        })
    )
    

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'country', 'postcode',
                  'town_or_city', 'street_address1', 'street_address2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            #'county': 'County, State or Locality',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

    def save(self, *args, **kwargs):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        customer, created = Customer.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            defaults=self.cleaned_data
        )
        self.instance.customer = customer
        return super().save(*args, **kwargs)

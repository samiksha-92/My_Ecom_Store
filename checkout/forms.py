from django import forms
from .models import Order, Customer


class OrderForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Full Name *',
            'class': 'stripe-style-input',
            'autofocus': True
        })
    )

    class Meta:
        model = Order
        fields = ('full_name', 'order_number', 'delivery_cost', 'order_total', 'grand_total',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on the first field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'order_number': 'Order Number',
            'delivery_cost': 'Delivery Cost',
            'order_total': 'Order Total',
            'grand_total': 'Grand Total',
        }

        for field in self.fields:
            if field != 'full_name':  # Skip full_name as it's already set up above
                self.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                self.fields[field].label = False

    def save(self, *args, **kwargs):
        """
        Override the save method to associate the order with a customer.
        """
        full_name = self.cleaned_data.get('full_name')
        customer, created = Customer.objects.get_or_create(full_name=full_name)
        self.instance.customer = customer
        return super().save(*args, **kwargs)


from django import forms
from .models import Profile
from django_countries.fields import CountryField

class ProfileForm(forms.ModelForm):
    country = CountryField().formfield(
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = [
            'default_phone_number',
            'default_country',
            'default_postcode',
            'default_town_or_city',
            'default_street_address1',
            'default_street_address2',
        ]

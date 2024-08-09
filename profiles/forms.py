from django import forms
from django_countries.fields import CountryField
from .models import Profile




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['default_phone_number', 'default_country', 'default_postcode', 'default_town_or_city', 'default_street_address1', 'default_street_address2']
        widgets = {
            'default_country': forms.Select(attrs={'class': 'form-control'}),
            'default_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'default_postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'default_town_or_city': forms.TextInput(attrs={'class': 'form-control'}),
            'default_street_address1': forms.TextInput(attrs={'class': 'form-control'}),
            'default_street_address2': forms.TextInput(attrs={'class': 'form-control'}),
        }

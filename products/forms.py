from django import forms
from .models import Product, Category,Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'sku']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']  
        widgets = {
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_review_text(self):
        review_text = self.cleaned_data.get('review_text')
        if not review_text.strip():  # Check if the review text is empty or only whitespace
            raise forms.ValidationError("You cannot submit an empty review.")
        return review_text
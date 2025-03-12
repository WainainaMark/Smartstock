from .models import Product, Stock
from django import forms

class SalesForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.values_list('name', flat=True).distinct(),  
        widget=forms.Select(attrs={'class': 'form-control'}),  # Optional styling
        empty_label="Select a product"
    )
    class Meta:
        model = Stock
        fields = ['product', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
        }
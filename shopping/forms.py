from django import forms

from .models import ShoppingItem


class ShoppingItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingItem
        fields = ['name', 'quantity', 'unit']

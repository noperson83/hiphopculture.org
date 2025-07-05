from django import forms
from .models import Return

class ShippingForm(forms.Form):
    DESTINATION_CHOICES = [
        ('USA', 'USA'),
        ('International', 'International'),
    ]
    destination = forms.ChoiceField(choices=DESTINATION_CHOICES, required=True)
    shipping_cost = forms.DecimalField(max_digits=6, decimal_places=2, required=False)

class RMAForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the reason for return'})
        }
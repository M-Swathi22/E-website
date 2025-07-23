from django import forms
from.models import Order


class OrderForm(forms.ModelForm):
    model = Order
    fields = ['full_name','mobile','address','payment_method']
    widgets = { 'address': forms.Textarea(attrs={'rows':3,'class':'form-control'}),'phone': forms.TextInput(attrs={'class':'form-control'}),}

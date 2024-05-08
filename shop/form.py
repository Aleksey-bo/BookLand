from django import forms
from .models import Order


class UserForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'country', 'phone_number', 'email', 'address']
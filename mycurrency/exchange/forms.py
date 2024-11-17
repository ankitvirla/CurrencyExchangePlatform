from django import forms
from .models import Currency

class CurrencyConversionForm(forms.Form):
    source_currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        label='Source Currency'
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Amount')
    target_currencies = forms.ModelMultipleChoiceField(
        queryset=Currency.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Target Currencies'
    )
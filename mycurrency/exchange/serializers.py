from rest_framework import serializers
from .models import Currency, CurrencyExchangeRate

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'symbol']

class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    source_currency = CurrencySerializer()
    exchanged_currency = CurrencySerializer()

    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'exchanged_currency', 'valuation_date', 'rate_value']
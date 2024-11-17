from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.code

class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(max_digits=18, decimal_places=6, db_index=True)

    def __str__(self):
        return f"{self.source_currency} to {self.exchanged_currency} on {self.valuation_date}"



class CurrencyConversion(models.Model):
    source_currency = models.ForeignKey(
        Currency, 
        related_name='source_conversions',  # Unique related_name for source_currency
        on_delete=models.CASCADE
    )
    exchanged_currency = models.ForeignKey(
        Currency, 
        related_name='exchanged_conversions',  # Unique related_name for exchanged_currency
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    converted_amount = models.DecimalField(decimal_places=2, max_digits=10)
    conversion_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} {self.source_currency} to {self.exchanged_currency} = {self.converted_amount}"
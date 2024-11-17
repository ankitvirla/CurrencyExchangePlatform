from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import path
from .models import Currency, CurrencyExchangeRate, CurrencyConversion

# Registering the Currency model with the @admin.register decorator
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol')  # Display these fields in the list view
    search_fields = ('code', 'name')  # Allow searching by code and name
    list_filter = ('name',)  # Add filtering options by name

# Registering the CurrencyExchangeRate model
@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('source_currency', 'exchanged_currency', 'valuation_date', 'rate_value')
    search_fields = ('source_currency__code', 'exchanged_currency__code', 'valuation_date')
    list_filter = ('valuation_date',)

# Registering the CurrencyConversion model
@admin.register(CurrencyConversion)
class CurrencyConversionAdmin(admin.ModelAdmin):
    list_display = ('source_currency', 'exchanged_currency', 'amount', 'converted_amount', 'conversion_date')
    search_fields = ('source_currency__code', 'exchanged_currency__code', 'amount')
    list_filter = ('conversion_date',)

# Custom CurrencyAdmin to add a custom link for currency converter view
class CurrencyAdminWithConverter(admin.ModelAdmin):
    change_list_template = 'admin/currency_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('convert/', self.admin_site.admin_view(self.convert_currency), name='currency_convert'),
        ]
        return custom_urls + urls

    def convert_currency(self, request):
        return HttpResponseRedirect(reverse('convert_currency'))
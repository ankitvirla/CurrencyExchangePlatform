from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import CurrencyExchangeRate, Currency, CurrencyConversion


class ExchangeRateService:
    def __init__(self, providers):
        """
        Initialize with a list of providers (e.g., CurrencyBeaconProvider, MockProvider).
        """
        self.providers = providers
    
    def get_exchange_rate_data(self, source_currency, start_date, end_date):
        rates = {}

        # Step 1: Try to fetch data from the backend (database)
        try:
            rates_query = CurrencyExchangeRate.objects.filter(
                source_currency__code=source_currency,
                valuation_date__range=[start_date, end_date]
            )

            # Collect rates for the given date range
            for rate in rates_query:
                date_str = rate.valuation_date.strftime('%Y-%m-%d')
                if date_str not in rates:
                    rates[date_str] = {}
                rates[date_str][rate.exchanged_currency.code] = rate.rate_value

            if rates:
                print("Returning data from the database.")
                return self.format_response(source_currency, start_date, end_date, rates)
        except Exception as e:
            print(f"Error fetching from backend: {e}")

        # Step 2: If no data is found in the backend, fall back to the providers
        provider = self.providers[0]  # CurrencyBeaconProvider (priority)
        try:
            rates = provider.get_exchange_rate_data(source_currency, start_date, end_date)
            self.insert_data_into_db(source_currency, rates, start_date, end_date)
            print("Returning data from the provider.")
            return self.format_response(source_currency, start_date, end_date, rates)
        except Exception as e:
            print(f"Provider failed: {e}")
            return self.format_response(source_currency, start_date, end_date, {})
    
    def insert_data_into_db(self, source_currency, rates, start_date, end_date):
        """
        Insert the fetched exchange rate data into the database for caching.
        """
        for date_str, rate_data in rates.items():
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Loop through each currency in the response data (e.g., EUR, GBP, INR)
            for exchanged_currency, rate_value in rate_data.items():
                try:
                    # Fetch the currencies from the database
                    #source_currency_obj = Currency.objects.get(code=source_currency)
                    #exchanged_currency_obj = Currency.objects.get(code=exchanged_currency)
                    
                    source_currency_obj, created = Currency.objects.get_or_create(code=source_currency)
                    # Fetch or create the exchanged currency
                    exchanged_currency_obj, created = Currency.objects.get_or_create(code=exchanged_currency)

                    # Insert the rate into the database
                    CurrencyExchangeRate.objects.create(
                        source_currency=source_currency_obj,
                        exchanged_currency=exchanged_currency_obj,
                        valuation_date=date_obj,
                        rate_value=rate_value
                    )
                    print(f"Inserted exchange rate for {source_currency} to {exchanged_currency} on {date_str}.")
                except ObjectDoesNotExist:
                    # If the currency doesn't exist, log the error and skip this entry
                    print(f"Currency {exchanged_currency} or {source_currency} does not exist in the database.")
                except Exception as e:
                    print(f"Error inserting data into DB: {e}")

    
    def format_response(self, source_currency, start_date, end_date, rates):
        return {
            "source_currency": source_currency,
            "date_range": {
                "from": start_date.strftime('%Y-%m-%d'),
                "to": end_date.strftime('%Y-%m-%d')
            },
            "rates": rates
        }
    
    def convert_amount(self, source_currency, amount, exchanged_currency):
        """
        Convert a given amount from source_currency to exchanged_currency.
        First, check the cache (database), and if not found, make an API call to get the conversion rate.
        """
        # Step 1: Check the cache (database) for existing conversion data
        try:
            conversion = CurrencyConversion.objects.get(
                source_currency__code=source_currency,
                exchanged_currency__code=exchanged_currency,
                amount=amount
            )
            print(f"Returning cached conversion for {amount} {source_currency} to {exchanged_currency}.")
            return conversion.converted_amount
        except CurrencyConversion.DoesNotExist:
            print(f"No cached conversion found for {amount} {source_currency} to {exchanged_currency}.")
        
        # Step 2: If no cached data, call the API to fetch the conversion rate
        provider = self.providers[0]  # CurrencyBeaconProvider (priority)
        try:
            converted_amount = provider.convert_amount(source_currency, amount, exchanged_currency)

            # Step 3: Cache the result (insert into the database) after successful API call
            self.insert_converted_data_into_db(source_currency, amount, exchanged_currency, converted_amount)
            return converted_amount
        except Exception as e:
            print(f"Provider failed: {e}")
            return None  # Return None or an appropriate error message

    def insert_converted_data_into_db(self, source_currency, amount, exchanged_currency, converted_amount):
        """
        Insert the conversion data into the database for future caching.
        """
        source_currency_obj = Currency.objects.get(code=source_currency)
        exchanged_currency_obj = Currency.objects.get(code=exchanged_currency)
        
        # Check if the conversion is already cached to avoid duplicates
        if not CurrencyConversion.objects.filter(
            source_currency=source_currency_obj,
            exchanged_currency=exchanged_currency_obj,
            amount=amount
        ).exists():
            # Insert the conversion into the database
            CurrencyConversion.objects.create(
                source_currency=source_currency_obj,
                exchanged_currency=exchanged_currency_obj,
                amount=amount,
                converted_amount=converted_amount
            )
            print(f"Inserted conversion rate into DB: {amount} {source_currency} to {converted_amount} {exchanged_currency}")

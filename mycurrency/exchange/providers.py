import os
import requests
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseProvider:
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        raise NotImplementedError
    
    def convert_amount(self, source_currency, amount, exchanged_currency):
        raise NotImplementedError

class CurrencyBeaconProvider:
    def __init__(self):
        self.api_key = os.environ.get('currencybeacon_key')
        self.base_url = "https://api.currencybeacon.com/v1"

    def get_exchange_rate_data(self, source_currency, start_date, end_date):
        """
        Fetch historical exchange rates for a given source_currency from CurrencyBeacon API
        between the start_date and end_date.
        """
        url = f"{self.base_url}/timeseries"
        rates = {}

        # Request data for the given date range
        response = requests.get(url, params={
            'base': source_currency,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'symbols': 'EUR,GBP,INR,JPY',  # Example: Include common currencies; you can modify this list
            'api_key': self.api_key
        })

        # Print the response status and body for debugging
        #print(f"Response Status: {response.status_code}")
        #print(f"Response Content: {response.text}")

        if response.status_code == 200:
            data = response.json()
            if 'response' in data and len(data['response']) > 0:
                for date_str, rate_data in data['response'].items():
                    rates[date_str] = rate_data
                return rates
            else:
                raise ValueError("No data found in the API response.")
        else:
            raise ValueError(f"Error fetching data from CurrencyBeacon API: {response.status_code} - {response.text}")
    def convert_amount(self, source_currency, amount, exchanged_currency):
        """
        Convert a given amount from source_currency to exchanged_currency using CurrencyBeacon API.
        """
        url = f"{self.base_url}/convert"
        
        response = requests.get(url, params={
            'from': source_currency,
            'to': exchanged_currency,
            'amount': amount,
            'api_key': self.api_key
        })

        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            data = response.json()
            if 'response' in data:
                converted_amount = data['response']['value']
                print(f"Converted {amount} {source_currency} to {converted_amount} {exchanged_currency}")
                return converted_amount
            else:
                raise ValueError("Error: 'converted_amount' not found in the response.")
        else:
            raise ValueError(f"Error fetching data from CurrencyBeacon API: {response.status_code} - {response.text}")
class MockProvider(BaseProvider):
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        print("Fetching from Mock provider...")
        return random.uniform(0.8, 1.5)  # Generate random rate
    
    def convert_amount(self, source_currency, amount, exchanged_currency):
        print("Converting using Mock provider...")
        return amount * random.uniform(0.8, 1.5)  # Simulate conversion

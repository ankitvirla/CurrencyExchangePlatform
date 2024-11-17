import asyncio
import aiohttp
from datetime import timedelta
from .models import Currency, CurrencyExchangeRate
from asgiref.sync import sync_to_async
import random

# Mock Data Function (optional if you want to simulate real-ish data)
def generate_mock_exchange_rate():
    # Return random exchange rates for testing purposes
    return random.uniform(0.5, 1.5)

# Function to fetch exchange rate data for a specific date from CurrencyBeacon
async def fetch_exchange_rate_data(session, url):
    print(f"Requesting URL: {url}")  # Debugging: print the URL
    async with session.get(url) as response:
        print(f"Response status: {response.status}")  # Debugging: check response status
        if response.status == 200:
            data = await response.json()
            print(f"Response data: {data}")  # Debugging: print response data
            return data
        else:
            print(f"Failed to fetch data from {url}, Status Code: {response.status}")
            return None

# Wrap the Django ORM operations in sync_to_async
@sync_to_async
def store_exchange_rate(base_currency, target_currency, current_date, rate_value):
    # Insert data into the database (CurrencyExchangeRate model)
    source_currency = Currency.objects.get(code=base_currency)
    target_currency_obj = Currency.objects.get(code=target_currency)
    
    # Insert into the model (if data doesn't already exist for that day)
    CurrencyExchangeRate.objects.update_or_create(
        source_currency=source_currency,
        exchanged_currency=target_currency_obj,
        valuation_date=current_date,
        defaults={'rate_value': rate_value}
    )
    print(f"Inserted data for {base_currency} to {target_currency} on {current_date.strftime('%Y-%m-%d')}: {rate_value}")

# Function to ingest historical exchange rates into the database
async def ingest_historical_data(base_currency, target_currencies, start_date, end_date, api_key):
    async with aiohttp.ClientSession() as session:
        current_date = start_date
        while current_date <= end_date:
            for target_currency in target_currencies:
                # Build the correct API URL
                url = f"https://api.currencybeacon.com/v1/historical?api_key={api_key}&base={base_currency}&date={current_date.strftime('%Y-%m-%d')}&symbol={target_currency}"
                
                # Fetch the exchange rate data for the day
                data = await fetch_exchange_rate_data(session, url)
                print(data)
                if data:
                    # Access the exchange rate data correctly from the response
                    rate_value = data['response']['rates'].get(target_currency)
                    
                    if not rate_value:
                        rate_value = generate_mock_exchange_rate()  # Generate mock data if no value is found
                    
                    # Store data in the database
                    await store_exchange_rate(base_currency, target_currency, current_date, rate_value)
                
            current_date += timedelta(days=1)  # Move to the next date

# Main function to run the asynchronous task
async def main(base_currency, target_currencies, start_date, end_date, api_key):
    await ingest_historical_data(base_currency, target_currencies, start_date, end_date, api_key)

def run_async_task(base_currency, target_currencies, start_date, end_date, api_key):
    asyncio.run(main(base_currency, target_currencies, start_date, end_date, api_key))

A Django-based platform for managing and retrieving currency exchange rates. This project allows users to fetch and store currency rates dynamically, convert amounts between currencies, and manage currencies and providers with a robust fallback mechanism. The project integrates external providers like CurrencyBeacon to fetch live exchange rates while maintaining flexibility to add other providers in the future.

## Features
### 1. Currency Rates List API
- **Retrieve Exchange Rates**: Fetch exchange rates for a specific time period from the database or external providers.
- **Fallback Mechanism**: Automatically fallback to active providers in priority order if data is unavailable in the database.

### 2. Convert Amount API
- **Currency Conversion**: Convert a given amount from one currency to another using the latest available exchange rate.
- **Dynamic Rate Fetching**: Automatically retrieve the rate from active providers if not cached.

### 3. Currency CRUD API
- **Manage Resources**: Dynamically manage currencies and providers via a REST API.
- **Admin Panel**: Leverage Django Admin for efficient CRUD operations.

### 4. Dynamic Provider Management
- **Adjust Provider Priority**: Change the priority of currency data providers.
- **Activate/Deactivate Providers**: Enable or disable providers at runtime.
- **Fallback Support**: Switch to the next available provider if the current one fails.

### 5. Admin Interface
- **User-Friendly Panel**: Manage currencies and providers through a simplified admin interface.
- **Integrated Conversion**: Directly convert amounts within the Django Admin interface.

### 6. Load Historical Data
- Custom Django management command to load historical exchange rate data efficiently.


##

## Prerequisites
- Python 3.11 or higher
- Django 4.x
- CurrencyBeacon API Key (or similar provider API key)
##

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ankitvirla/CurrencyExchangePlatform.git
cd currency-exchange
```

### 2. Create a Virtual Environment
```bash
python3.11 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
currencybeacon_key=<your_currency_beacon_api_key>
```

### 5. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Access the platform at http://127.0.0.1:8000/

##

## API Endpoints

### 1. Currency Rates List
Endpoint: /api/currency-rates/
Method: GET
Parameters: 
- source_currency (e.g., USD)
- date_from (YYYY-MM-DD)
- date_to (YYYY-MM-DD)

Example Request:
```bash
GET http://127.0.0.1:8000/api/currency-rates/?source_currency=USD&date_from=2023-01-01&date_to=2023-01-31
```

Example Response:
```bash
{
    "source_currency": "USD",
    "date_range": {
        "from": "2024-11-01",
        "to": "2024-11-10"
    },
    "rates": {
        "2024-11-01": {
            "EUR": 0.919143,
            "GBP": 0.773581,
            "INR": 84.110776,
            "JPY": 153.019481
        },
    ...}
}

```
### 2. Convert Amount
Endpoint: /currency-amount/
Method: GET
Parameters:
- source_currency
- exchanged_currency
- amount

Example Request:
```bash
GET http://127.0.0.1:8000/convert/?source_currency=USD&exchanged_currency=EUR&amount=100
```

Example Response:
```bash
{
    "converted_amount": 84.47
}
```
### 3. Currency CRUD
Endpoint: /api/currencies/
Method: GET, POST, PUT, DELETE

Example Request:
```bash
POST http://127.0.0.1:8000/api/currencies/
Content-Type: application/json

{"code": "MYR", "name": "Malaysian ringgi", "symbol": "Ringgit"}

```

### 4. Load Historical Data
A custom Django management command allows you to load historical exchange rates from providers or other sources efficiently.
## Usage
- Run the following command:
```bash
python manage.py load_historical_data --base USD --targets INR,EUR,GBP --start 2024-01-01 --end 2024-01-10 --api-key 12xy
```
- Parameters:
  - --source_currency: The base currency for the exchange rates (e.g., USD)
  - --target_currency: The target currency for the exchange rates (e.g., EUR).
  - --start_date: The start date for historical data (format: YYYY-MM-DD).
  - --end_date: The end date for historical data (format: YYYY-MM-DD).

- The command will:
    - Fetch data from active providers.
    - Save the data in the CurrencyRate table for future use.
  Example Execution:
```bash
python manage.py load_historic_data --source_currency=USD --target_currency=EUR --start_date=2023-01-01 --end_date=2023-01-31
```
##

## Convert View
Access the Convert View at http://localhost:8000/convert/

### Convert Amount Section
- Navigate to the Currency Rates section
- Use the Convert Amount tool to calculate conversions directly from the admin interface.
##

## Major Implementation Details
### 1.  ExchangeRateService
A core service that fetches exchange rates from:
- Database: Returns cached data if available.
- External Providers: Iterates over active providers based on priority to fetch live rates.
- Fallback Mechanism: If one provider fails, the next provider is used.

### 2. Dynamic Provider Management
Providers can be managed dynamically using the Provider model:
- Activate/Deactivate Providers: Toggle is_active in the admin.
- Change Priority: Adjust the priority field to reorder provider usage.

### 3. Admin Integration
Custom admin views and templates allow administrators to:
- Use the Convert Amount feature directly from the admin interface.
- Manage currencies and providers seamlessly.

##
## Troubleshooting
### Issues Faced
### 1. KeyError: 'currencies':
- Resolved by adapting the response structure for the CurrencyBeacon API, which used a response key instead of currencies.

### 2. Missing Installed App:
- Fixed by ensuring the exchange app was added to the INSTALLED_APPS list in settings.py.

### 3. Empty API Responses:
- Resolved by implementing a fallback mechanism to fetch rates dynamically from providers.

## Debugging Steps
- Use print() statements to debug provider responses in providers.py.
- Verify API keys and query parameters using Postman.
- Check the database for cached rates using the Django shell:
```bash
python manage.py shell
>>> from exchange.models import CurrencyRate
>>> CurrencyRate.objects.all()
```
##
## Future Improvements
- Asynchronous Data Loading: Use Celery and Redis to load historical data in bulk.
- Enhanced Caching: Implement Redis or Django’s caching framework for faster responses.
- API Versioning: Add versioning support to the REST API.
- Frontend Integration: Build a frontend interface for end users.

 




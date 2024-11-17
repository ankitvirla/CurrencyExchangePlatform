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
##

## Prerequisites
- Python 3.11 or higher
- Django 4.x
- CurrencyBeacon API Key (or similar provider API key)
##

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
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
##



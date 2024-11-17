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


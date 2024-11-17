from .providers import CurrencyBeaconProvider, MockProvider

def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider="CurrencyBeacon"):
    if provider == "CurrencyBeacon":
        return CurrencyBeaconProvider().get_exchange_rate_data(source_currency, exchanged_currency, valuation_date)
    elif provider == "Mock":
        return MockProvider().get_exchange_rate_data(source_currency, exchanged_currency, valuation_date)
    else:
        raise ValueError("Unknown provider")
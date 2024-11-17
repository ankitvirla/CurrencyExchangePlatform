from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

#importing files
from .service import ExchangeRateService
from .providers import CurrencyBeaconProvider, MockProvider
from .models import Currency
from .serializers import CurrencySerializer
from .forms import CurrencyConversionForm

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CurrencyRatesListView(APIView):
    def get(self, request, *args, **kwargs):
        source_currency = request.query_params.get('source_currency')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        # Validate query parameters
        if not source_currency or not date_from or not date_to:
            return Response(
                {"error": "Missing required query parameters: source_currency, date_from, date_to"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to parse the date parameters
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Please use YYYY-MM-DD for date_from and date_to."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Initialize provider service with providers sorted by priority
        providers = [CurrencyBeaconProvider(), MockProvider()]
        service = ExchangeRateService(providers)  # Pass providers as an argument here

        # Get the exchange rates from the service
        rates = service.get_exchange_rate_data(source_currency, date_from, date_to)

        return Response(rates, status=status.HTTP_200_OK)


class CurrencyConverterView(APIView):
    def get(self, request, *args, **kwargs):
        source_currency = request.query_params.get('source_currency')
        amount = request.query_params.get('amount')
        exchanged_currency = request.query_params.get('exchanged_currency')

        # Validate query parameters
        if not source_currency or not amount or not exchanged_currency:
            return Response(
                {"error": "Missing required query parameters: source_currency, amount, exchanged_currency"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = float(amount)  # Ensure the amount is a valid number
        except ValueError:
            return Response(
                {"error": "Invalid amount format. Please provide a valid number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Initialize provider service with providers sorted by priority
        providers = [CurrencyBeaconProvider(), MockProvider()]
        service = ExchangeRateService(providers)

        # Get the converted amount from the service
        try:
            converted_amount = service.convert_amount(source_currency, amount, exchanged_currency)
            if converted_amount is None:
                return Response({"error": "Conversion failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"converted_amount": converted_amount}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Conversion failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def convert_currency(request):
    # Handle form submission
    if request.method == 'POST':
        form = CurrencyConversionForm(request.POST)
        if form.is_valid():
            source_currency = form.cleaned_data['source_currency']
            amount = form.cleaned_data['amount']
            target_currencies = form.cleaned_data['target_currencies']

            # Use the provider to convert
            provider = CurrencyBeaconProvider()
            conversion_results = {}

            for target_currency in target_currencies:
                # Get conversion from the provider (assuming convert_amount is defined)
                converted_amount = provider.convert_amount(source_currency.code, amount, target_currency.code)
                conversion_results[target_currency] = converted_amount

            return render(request, 'conversion_result.html', {
                'source_currency': source_currency,
                'amount': amount,
                'conversion_results': conversion_results
            })
    else:
        form = CurrencyConversionForm()

    return render(request, 'convert_currency.html', {'form': form})
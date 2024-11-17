from django.core.management.base import BaseCommand
from exchange.tasks import run_async_task
from datetime import datetime

class Command(BaseCommand):
    help = 'Load historical exchange rate data asynchronously for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument('--base', type=str, help='Base currency (e.g., USD)')
        parser.add_argument('--targets', type=str, help='Comma-separated list of target currencies (e.g., EUR,GBP)')
        parser.add_argument('--start', type=str, help='Start date for historical data (e.g., 2024-01-01)')
        parser.add_argument('--end', type=str, help='End date for historical data (e.g., 2024-01-10)')
        parser.add_argument('--api-key', type=str, help='API key for authentication')

    def handle(self, *args, **kwargs):
        base_currency = kwargs['base']
        target_currencies = kwargs['targets'].split(',')
        start_date = kwargs['start']
        end_date = kwargs['end']
        api_key = kwargs['api_key']

        # Convert string date to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Call the asynchronous task with the provided arguments
        run_async_task(base_currency, target_currencies, start_date, end_date, api_key)
        self.stdout.write(self.style.SUCCESS('Successfully fetched historical data'))
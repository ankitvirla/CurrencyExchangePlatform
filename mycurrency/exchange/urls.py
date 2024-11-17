from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyRatesListView, CurrencyViewSet,CurrencyConverterView
from . import views

router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet)

urlpatterns = [
    path('currency-rates/', CurrencyRatesListView.as_view(), name='currency_rates_list'),
    path('currency-amount/', CurrencyConverterView.as_view(), name='currency_amount'),
    path('api/', include(router.urls)),
    path('convert/', views.convert_currency, name='convert_currency'),
]

from django.urls import path

from .views import CreatePaymentUrl, PaymentHandler

urlpatterns = [
    path('api/invoice/create', CreatePaymentUrl.as_view(), name='create-payment'),
    path('api/invoice/payment-handler', PaymentHandler.as_view(), name='payment-handler'),
]

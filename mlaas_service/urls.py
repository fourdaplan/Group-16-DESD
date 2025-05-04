# mlaas_service/urls.py

from django.urls import path
from .views import predict_settlement

urlpatterns = [
    path('predict-core-model/', predict_settlement, name='predict_core_model'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillingViewSet, finance_dashboard_view  #  Import the dashboard view

router = DefaultRouter()
router.register(r'billing', BillingViewSet, basename='billing')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', finance_dashboard_view, name='finance_dashboard'),  #   Add this line
]

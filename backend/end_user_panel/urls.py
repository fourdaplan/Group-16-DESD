from django.urls import path
from . import views
from .views import list_end_users, download_invoice_csv


urlpatterns = [
    path('upload/', views.upload_file_view, name='upload_file'),
    path('list-users/', list_end_users, name='list_end_users'),
    path('invoice/', download_invoice_csv, name='download_invoice_csv'),
    # Add more endpoints here in the future if needed
]

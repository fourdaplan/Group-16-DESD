from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),  # 👈 Add this line
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('ai-dashboard/', views.ai_dashboard, name='ai_dashboard'),
    path('finance-dashboard/', views.finance_dashboard, name='finance_dashboard'),
    path('end-user-dashboard/', views.end_user_dashboard, name='end_user_dashboard'),
    path('register/', views.end_user_register, name='register'),

]

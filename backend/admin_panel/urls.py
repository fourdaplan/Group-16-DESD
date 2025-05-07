from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ActivityLogViewSet,
    admin_dashboard,
    approve_engineer,
    view_activity_logs,
)

# DRF router for API
router = DefaultRouter()
router.register(r'logs', ActivityLogViewSet, basename='activity-log')

# Combine API + template views
urlpatterns = [
    path('', include(router.urls)),  # API: /admin-panel/logs/
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('approve/<int:user_id>/', approve_engineer, name='approve_engineer'),
    path('activity-logs/', view_activity_logs, name='view_activity_logs'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ActivityLogViewSet,
    admin_dashboard,
    approve_engineer,
    view_activity_logs,
    user_list,
    add_user,
    edit_user,
    delete_user,
)

# DRF router for API
router = DefaultRouter()
router.register(r'logs', ActivityLogViewSet, basename='activity-log')

urlpatterns = [
    path('', include(router.urls)),  # API: /admin-panel/logs/
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('approve/<int:user_id>/', approve_engineer, name='approve_engineer'),
    path('activity-logs/', view_activity_logs, name='view_activity_logs'),

    # ✅ User Management URLs
    path('users/', user_list, name='user_list'),
    path('users/add/', add_user, name='add_user'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
]

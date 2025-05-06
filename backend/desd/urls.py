from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from dashboard import views as dashboard_views

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # API Routes
    path('api/', include('billing.urls')),
    path('api/models/', include('model_manager.urls')),
    path('api/end-user/', include('end_user_panel.urls')),
    path('api/admin/', include('admin_panel.urls')),
    path('api/core-model/', include('mlaas_service.urls')),


    # User-facing Dashboards (handled via dashboard/views.py)
    path('end-user-dashboard/', dashboard_views.end_user_dashboard, name='end_user_dashboard'),
    path('admin-dashboard/', dashboard_views.admin_dashboard, name='admin_dashboard'),
    path('ai-dashboard/', dashboard_views.ai_dashboard, name='ai_dashboard'),
    path('finance-dashboard/', dashboard_views.finance_dashboard, name='finance_dashboard'),
    path('login/', dashboard_views.custom_login, name='login'),

    # ✅ Add main dashboard route here
    path('main-dashboard/', dashboard_views.main_dashboard, name='main_dashboard'),
]


# Serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL configuration for desd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
import os
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/', include('admin_panel.urls')),
    path('admin-dashboard/', serve, {
        'path': 'index.html',
        'document_root': os.path.join(settings.BASE_DIR, 'admin_dashboard'),
    }),
    path('api/', include('billing.urls')),
    path('api/end-user/', include('end_user_panel.urls')),
    path('end-user-dashboard/', serve, {
        'path': 'enduserdash.html',
        'document_root': os.path.join(settings.BASE_DIR, 'end_user_dashboard'),
    }),
    path('api/models/', include('model_manager.urls')),
    path('ai-dashboard/', serve, {
        'path': 'index.html',
        'document_root': os.path.join(settings.BASE_DIR, 'ai_engineer_dashboard'),
    }),
    path('finance-dashboard/', serve, {
        'path': 'financedashboard.html',
        'document_root': os.path.join(settings.BASE_DIR, 'finance_dashboard'),
    }),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
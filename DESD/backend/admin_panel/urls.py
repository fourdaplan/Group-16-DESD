from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityLogViewSet

router = DefaultRouter()
router.register(r'logs', ActivityLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

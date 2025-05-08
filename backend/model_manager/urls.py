from django.urls import path
from .views import (
    UploadedModelListCreateView,
    UploadedModelDetailView,
    UserModelListView,
    ActivateModelView,
    FeedbackListView
)

urlpatterns = [
    path('', UploadedModelListCreateView.as_view(), name='model-list-create'),
    path('<int:pk>/', UploadedModelDetailView.as_view(), name='model-detail'),
    path('my-models/', UserModelListView.as_view(), name='user-models'),
    path('activate/<int:pk>/', ActivateModelView.as_view(), name='activate-model'),
    path('feedback/', FeedbackListView.as_view(), name='feedback-list'),  # NEW
]

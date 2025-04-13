from rest_framework import viewsets, permissions
from .models import UploadedModel
from .serializers import UploadedModelSerializer

class IsAIEngineer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name="AI Engineers").exists()

class UploadedModelViewSet(viewsets.ModelViewSet):
    queryset = UploadedModel.objects.all().order_by('-uploaded_at')
    serializer_class = UploadedModelSerializer
    permission_classes = [IsAIEngineer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

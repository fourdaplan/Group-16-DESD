from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedModel
from .serializers import UploadedModelSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status


class UploadedModelListCreateView(generics.ListCreateAPIView):
    queryset = UploadedModel.objects.all()
    serializer_class = UploadedModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UploadedModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UploadedModel.objects.all()
    serializer_class = UploadedModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserModelListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        models = UploadedModel.objects.filter(user=user)
        serializer = UploadedModelSerializer(models, many=True)
        return Response(serializer.data)


class ActivateModelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            model_to_activate = UploadedModel.objects.get(pk=pk, user=request.user)
            UploadedModel.objects.filter(user=request.user).update(active=False)
            model_to_activate.active = True
            model_to_activate.save()
            return Response({"message": "Model activated successfully."})
        except UploadedModel.DoesNotExist:
            return Response({"error": "Model not found."}, status=status.HTTP_404_NOT_FOUND)

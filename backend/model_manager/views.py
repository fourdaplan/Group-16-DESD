from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User

from .models import UploadedModel
from end_user_panel.models import UploadedFile
from .serializers import UploadedModelSerializer

class UploadedModelListCreateView(generics.ListCreateAPIView):
    queryset = UploadedModel.objects.all()
    serializer_class = UploadedModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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


# NEW: Feedback listing view
class FeedbackListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        feedbacks = UploadedFile.objects.filter(feedback__isnull=False).order_by('-uploaded_at')
        feedback_data = [{
            "user": feedback.user.username,
            "file_name": feedback.file.name,
            "uploaded_at": feedback.uploaded_at,
            "feedback": feedback.feedback
        } for feedback in feedbacks]

        return Response(feedback_data)

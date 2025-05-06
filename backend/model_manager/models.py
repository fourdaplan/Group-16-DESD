# model_manager/models.py
from django.db import models
from django.contrib.auth.models import User

class UploadedModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    model_file = models.FileField(upload_to='ai_models/')
    preprocessor_file = models.FileField(upload_to='ai_models/', blank=True, null=True)
    cluster_model_file = models.FileField(upload_to='ai_models/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    r2_score = models.FloatField(null=True, blank=True)
    rmse = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} by {self.user.username}"

class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(UploadedModel, on_delete=models.CASCADE, related_name='interactions')
    input_data = models.TextField()
    output_data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interaction with {self.model.name} at {self.timestamp}"

from django.db import models
from django.contrib.auth.models import User

class UploadedModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_file = models.FileField(upload_to='ai_models/')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user.username}"

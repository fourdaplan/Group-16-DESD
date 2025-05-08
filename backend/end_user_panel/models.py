from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track who uploaded the file
    file = models.FileField(upload_to='uploads/')  # Stores the uploaded file
    file_type = models.CharField(max_length=50)  # e.g., 'text', 'image', 'audio'
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for uploads

    # NEW FIELDS
    predicted_settlement = models.FloatField(null=True, blank=True)
    cluster = models.CharField(max_length=50, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)  # Optional user feedback

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"

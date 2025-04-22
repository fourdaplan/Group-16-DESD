from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Stores the uploaded file
    file_type = models.CharField(max_length=50)  # File type info
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"File {self.id} uploaded at {self.uploaded_at}"

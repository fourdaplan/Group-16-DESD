
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Store the uploaded file
    file_type = models.CharField(max_length=50)  # To store the file type (image, audio, etc.)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the file was uploaded

    def __str__(self):
        return f"File {self.id} uploaded at {self.uploaded_at}"

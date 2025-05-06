from django.db import models
from django.contrib.auth.models import User

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"
class MLUsageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    action_type = models.CharField(max_length=50, choices=[
        ("prediction", "Prediction"),
        ("training", "Training"),
        ("upload", "Upload"),
    ])
    input_summary = models.TextField(blank=True, null=True)  # Optional: Summary of input
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action_type} on {self.model_name} at {self.timestamp}"

from django.db import models
from django.contrib.auth.models import User

class BillingRecord(models.Model):
    ACTION_CHOICES = [
        ('prediction', 'Prediction'),
        # add other actions here as needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.action} – {self.cost}"

class SystemLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    detail = models.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp} | {self.user.username} | {self.action}"


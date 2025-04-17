from django.db import models
from django.contrib.auth.models import User

class BillingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)  # e.g. 'prediction'
    timestamp = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2)  # e.g. 0.50

    def __str__(self):
        return f"{self.user.username} - {self.action} - ${self.cost} @ {self.timestamp}"

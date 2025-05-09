from rest_framework import serializers
from .models import BillingRecord

class BillingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingRecord
        fields = ["id", "user", "action", "cost", "timestamp"]

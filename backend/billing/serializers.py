from rest_framework import serializers
from .models import BillingRecord

class BillingRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = BillingRecord
        fields = '__all__'

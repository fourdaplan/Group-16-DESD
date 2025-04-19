from rest_framework import serializers
from .models import UploadedModel

class UploadedModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UploadedModel
        fields = '__all__'
        read_only_fields = ['user', 'uploaded_at']

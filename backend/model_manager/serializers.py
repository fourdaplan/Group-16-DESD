from rest_framework import serializers
from .models import UploadedModel, Interaction

class UploadedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedModel
        fields = [
            'id',
            'user',
            'model_file',
            'name',
            'description',
            'uploaded_at',
            'active',
            'r2_score',
            'rmse',
            'preprocessor_file',
            'cluster_model_file'
        ]
        read_only_fields = ['user', 'uploaded_at', 'active', 'id']
class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = [
            'id',
            'model',
            'input_data',
            'prediction_result',
            'timestamp'
        ]

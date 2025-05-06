from django.contrib import admin
from .models import UploadedModel

@admin.register(UploadedModel)
class UploadedModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'uploaded_at', 'active')
    list_filter = ('active', 'uploaded_at')

from django.contrib import admin
from .models import UploadedFile

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'uploaded_at', 'predicted_settlement', 'cluster', 'feedback')
    search_fields = ('user__username', 'file', 'feedback')

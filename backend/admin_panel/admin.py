from django.contrib import admin
from .models import ActivityLog, MLUsageLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    search_fields = ('user__username', 'action')

@admin.register(MLUsageLog)
class MLUsageLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'model_name', 'action_type', 'timestamp')
    search_fields = ('user__username', 'model_name', 'action_type')

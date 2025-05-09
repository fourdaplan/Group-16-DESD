from django.contrib import admin
from .models import BillingRecord, SystemLog

@admin.register(BillingRecord)
class BillingRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'action', 'cost')
    list_filter = ('user', 'timestamp', 'action')
    search_fields = ('user__username', 'action')

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'detail')
    list_filter = ('action', 'user', 'timestamp')
    search_fields = ('user__username', 'action', 'detail')

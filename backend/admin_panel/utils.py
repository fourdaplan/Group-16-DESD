from .models import ActivityLog

def log_activity(user, action):
    if user and user.is_authenticated:
        ActivityLog.objects.create(user=user, action=action)

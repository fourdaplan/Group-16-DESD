# admin_panel/signals.py

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .utils import log_activity


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    log_activity(user, "Logged in")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    log_activity(user, "Logged out")

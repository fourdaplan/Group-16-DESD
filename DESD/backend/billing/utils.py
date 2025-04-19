from .models import BillingRecord

def create_billing_record(user, action, cost):
    if user and user.is_authenticated:
        BillingRecord.objects.create(user=user, action=action, cost=cost)

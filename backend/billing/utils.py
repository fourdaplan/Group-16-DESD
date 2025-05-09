from .models import BillingRecord

def create_billing_record(user, action, cost):
    BillingRecord.objects.create(
        user=user,
        action=action,
        cost=cost
    )

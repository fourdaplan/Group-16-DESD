from rest_framework import viewsets, permissions
from .models import BillingRecord
from .serializers import BillingRecordSerializer
from django.db.models import Sum, Count
from rest_framework.decorators import action
from rest_framework.response import Response

class BillingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BillingRecord.objects.all().order_by('-timestamp')
    serializer_class = BillingRecordSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        data = BillingRecord.objects.values('user__username') \
            .annotate(
                total_actions=Count('id'),
                total_due=Sum('cost')
            ).order_by('-total_due')

        return Response(data)

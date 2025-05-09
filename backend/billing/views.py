from django.db.models import F, Sum, Count
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import csv
import logging
import requests
from .models import BillingRecord, SystemLog
from .serializers import BillingRecordSerializer
from django.utils import timezone
from django.contrib.auth.models import User  # ✅ Import User for group filtering

logger = logging.getLogger(__name__)

class BillingViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def summary(self, request):
        if not (
            request.user.groups.filter(name='Finance').exists() or
            request.user.groups.filter(name='Admin').exists() or
            request.user.is_superuser or
            request.user.is_staff
        ):
            return Response({"detail": "Access denied. You must be a finance or admin user."}, status=status.HTTP_403_FORBIDDEN)

        # ✅ Only include records for users in the 'end users' group
        end_user_ids = User.objects.filter(groups__name="end users").values_list("id", flat=True)
        qs = BillingRecord.objects.filter(user__id__in=end_user_ids)

        start = request.query_params.get("start_date")
        end = request.query_params.get("end_date")
        filter_user = request.query_params.get("username")

        if start:
            qs = qs.filter(timestamp__gte=start)
        if end:
            qs = qs.filter(timestamp__lte=end)
        if filter_user:
            qs = qs.filter(user__username=filter_user)

        data = (
            qs
            .values(username=F("user__username"))
            .annotate(total_actions=Count("id"), total_due=Sum("cost"))
            .order_by("-total_due")
        )

        SystemLog.objects.create(
            user=request.user,
            action="Load Billing Summary",
            detail=f"start={start}, end={end}, username={filter_user or 'all'}"
        )

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def invoice(self, request):
        username_param = request.query_params.get("username")

        if username_param and (
            request.user.groups.filter(name='Finance').exists() or
            request.user.groups.filter(name='Admin').exists() or
            request.user.is_superuser or
            request.user.is_staff
        ):
            try:
                user = User.objects.get(username=username_param)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user

        start = request.query_params.get("start_date")
        end = request.query_params.get("end_date")

        qs = BillingRecord.objects.filter(user=user)
        if start:
            qs = qs.filter(timestamp__gte=start)
        if end:
            qs = qs.filter(timestamp__lte=end)

        records = qs.values("timestamp", "action", "cost").order_by("timestamp")
        total = qs.aggregate(total_due=Sum("cost"))["total_due"] or 0

        SystemLog.objects.create(
            user=request.user,
            action="View Invoice Page",
            detail=f"for={user.username}, start={start}, end={end}"
        )

        return render(request, "billing/invoice_template.html", {
            "user": user,
            "start": start,
            "end": end,
            "records": records,
            "total": total
        })

    @action(detail=False, methods=["get"], url_path="export", permission_classes=[permissions.IsAuthenticated])
    def export_csv(self, request):
        if not (
            request.user.groups.filter(name='Finance').exists() or
            request.user.groups.filter(name='Admin').exists() or
            request.user.is_superuser or
            request.user.is_staff
        ):
            return Response({"detail": "Access denied. You must be a finance or admin user."}, status=status.HTTP_403_FORBIDDEN)

        start = request.query_params.get("start_date")
        end = request.query_params.get("end_date")
        qs = BillingRecord.objects.all()
        if start:
            qs = qs.filter(timestamp__gte=start)
        if end:
            qs = qs.filter(timestamp__lte=end)

        summary = (
            qs.values("user__username")
            .annotate(total_actions=Count("id"), total_due=Sum("cost"))
            .order_by("user__username")
        )

        SystemLog.objects.create(
            user=request.user,
            action="Export CSV",
            detail=f"start={start}, end={end}"
        )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="billing_summary.csv"'

        writer = csv.writer(response)
        writer.writerow(['Username', 'Total Actions', 'Total Due'])
        for row in summary:
            writer.writerow([
                row["user__username"],
                row["total_actions"],
                format(row["total_due"] or 0, ".2f")
            ])

        return response

    @action(detail=False, methods=["post"], url_path="send-to-billing", permission_classes=[permissions.IsAuthenticated])
    def send_to_billing(self, request):
        username = request.data.get("username")
        if not username:
            return Response({"error": "Username is required."}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        qs = BillingRecord.objects.filter(user=user)
        total = qs.aggregate(total_due=Sum("cost"))["total_due"] or 0
        summary = {
            "username": user.username,
            "total_due": f"{total:.2f}",
            "invoice_id": f"{user.username}-INV-{timezone.now().strftime('%Y%m%d%H%M')}"
        }

        mock_url = "https://httpbin.org/post"
        response = requests.post(mock_url, json=summary)

        SystemLog.objects.create(
            user=request.user,
            action="Send Invoice to Billing Provider",
            detail=f"invoice_for={user.username}, status={response.status_code}"
        )

        return Response({
            "status": "sent",
            "billing_service_response": response.json()
        }, status=response.status_code)


@login_required
def finance_dashboard_view(request):
    if not (
        request.user.groups.filter(name='Finance').exists() or
        request.user.is_superuser or
        request.user.is_staff
    ):
        return HttpResponse("Access Denied", status=403)

    start = request.GET.get("start_date")
    end = request.GET.get("end_date")
    filter_user = request.GET.get("username")

    qs = BillingRecord.objects.all()

    if start:
        qs = qs.filter(timestamp__gte=start)
    if end:
        qs = qs.filter(timestamp__lte=end)
    if filter_user:
        qs = qs.filter(user__username=filter_user)

    summary = (
        qs.values("user__username")
        .annotate(total_actions=Count("id"), total_due=Sum("cost"))
        .order_by("-total_due")
    )

    recent_records = qs.order_by("-timestamp")[:10]

    context = {
        "summary": summary,
        "recent_records": recent_records,
        "start": start,
        "end": end,
        "filter_user": filter_user,
    }

    return render(request, 'finance_dashboard/financedashboard.html', context)

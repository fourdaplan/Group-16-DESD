import csv
import io
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
from billing.models import BillingRecord  #  Import BillingRecord model
from admin_panel.utils import log_activity  #  Import logging utility
from django.contrib.auth.models import Group, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from billing.models import BillingRecord  # import BillingRecord
from django.utils import timezone


def clean_csv_record(record):
    expected_fields = [
        "accident_type", "injury_prognosis", "special_health_expenses", "special_reduction", "special_overage",
        "general_rest", "special_additional_injury", "special_earnings_loss", "special_usage_loss",
        "special_medications", "special_asset_damage", "special_rehabilitation", "special_fixes", "general_fixed",
        "general_uplift", "special_loaner_vehicle", "special_trip_costs", "special_journey_expenses",
        "special_therapy", "exceptional_circumstances", "minor_psychological_injury", "dominant_injury", "whiplash",
        "vehicle_type", "weather_conditions", "vehicle_age", "driver_age", "number_of_passengers",
        "accident_description", "injury_description", "police_report_filed", "witness_present", "gender",
        "days_to_claim"
    ]

    cleaned = {k: record[k] for k in expected_fields if k in record}

    float_fields = [
        "special_health_expenses", "special_reduction", "special_overage", "general_rest",
        "special_additional_injury", "special_earnings_loss", "special_usage_loss",
        "special_medications", "special_asset_damage", "special_rehabilitation", "special_fixes",
        "general_fixed", "general_uplift", "special_loaner_vehicle", "special_trip_costs",
        "special_journey_expenses", "special_therapy"
    ]

    int_fields = ["vehicle_age", "driver_age", "number_of_passengers", "days_to_claim"]

    for f in float_fields:
        cleaned[f] = float(record.get(f, 0) or 0)

    for f in int_fields:
        cleaned[f] = int(record.get(f, 0) or 0)

    return cleaned


@login_required
@csrf_protect
def upload_file_view(request):
    prediction = None
    group = None
    error = None
    success_message = None

    if request.user.groups.filter(name='end users').exists():
        request.session['role'] = 'end_user'

    uploaded_files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')

    if request.method == 'POST':
        if request.POST.get("feedback_only"):
            feedback_text = request.POST.get("feedback")
            latest_file = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at').first()

            if latest_file:
                latest_file.feedback = feedback_text
                latest_file.save()
                success_message = " Feedback submitted successfully!"
                log_activity(request.user, f"Submitted feedback: \"{feedback_text}\"")
            else:
                error = "❌ No uploaded file to attach feedback to."

            return render(request, 'end_user_dashboard/enduserdash.html', {
                'success': True,
                'prediction': prediction,
                'group': group,
                'error': error,
                'uploaded_files': uploaded_files,
                'success_message': success_message if not error else None
            })

        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            file_type = uploaded_file.content_type.split('/')[0]

            try:
                file_data = uploaded_file.read().decode('utf-8')
                uploaded_file.seek(0)

                uploaded_file_obj = UploadedFile.objects.create(
                    file=uploaded_file,
                    file_type=file_type,
                    user=request.user
                )
                log_activity(request.user, f"Uploaded file: {uploaded_file.name}")

                reader = csv.DictReader(io.StringIO(file_data))
                record = next(reader)
                cleaned_record = clean_csv_record(record)

            except Exception as e:
                error = f"CSV error: {e}"
                return render(request, 'end_user_dashboard/enduserdash.html', {
                    'error': error,
                    'uploaded_files': uploaded_files
                })

            try:
                response = requests.post('http://mlaas-service:9000/predict/', json=cleaned_record)
                if response.status_code == 200:
                    data = response.json()
                    prediction = data.get('predicted_settlement')
                    group = data.get('cluster')

                    uploaded_file_obj.predicted_settlement = prediction
                    uploaded_file_obj.cluster = group
                    uploaded_file_obj.save()

                    #  Save billing record
                    BillingRecord.objects.create(
                        user=request.user,
                        action="ML prediction request",
                        cost=prediction or 0
                    )

                    log_activity(request.user, f"Prediction made: £{prediction}, Cluster: {group}")

                else:
                    error = f"API Error: {response.status_code}"
            except Exception as e:
                error = f"Request failed: {e}"

    return render(request, 'end_user_dashboard/enduserdash.html', {
        'success': prediction is not None,
        'prediction': prediction,
        'group': group,
        'error': error,
        'uploaded_files': uploaded_files,
        'success_message': success_message
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_end_users(request):
    try:
        group = Group.objects.get(name='end users')
        users = group.user_set.all().values('username')
        return Response(list(users))
    except Group.DoesNotExist:
        return Response([], status=200)

@login_required
def download_invoice_csv(request):
    user = request.user
    records = BillingRecord.objects.filter(user=user)

    if not records.exists():
        return HttpResponse("❌ No billing records found for you.", status=404)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user.username}_invoice.csv"'

    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Action', 'Cost'])

    for record in records:
        writer.writerow([record.timestamp.strftime('%Y-%m-%d %H:%M'), record.action, f"£{record.cost:.2f}"])

    return response

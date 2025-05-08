import csv
import io
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
from admin_panel.utils import log_activity  # ✅ Import logging utility


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

    # ✅ Set session role if user belongs to end user group
    if request.user.groups.filter(name='end users').exists():
        request.session['role'] = 'end_user'

    uploaded_files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')

    if request.method == 'POST':
        # ✅ Feedback submission
        if request.POST.get("feedback_only"):
            feedback_text = request.POST.get("feedback")
            latest_file = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at').first()

            if latest_file:
                latest_file.feedback = feedback_text
                latest_file.save()
                success_message = "✅ Feedback submitted successfully!"
                log_activity(request.user, f"Submitted feedback: \"{feedback_text}\"")  # ✅ Log feedback
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

        # ✅ File upload for prediction
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
                log_activity(request.user, f"Uploaded file: {uploaded_file.name}")  # ✅ Log upload

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

                    log_activity(request.user, f"Prediction made: £{prediction}, Cluster: {group}")  # ✅ Log prediction

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

import csv
import io
import requests
from django.shortcuts import render
from .models import UploadedFile
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

@login_required
@csrf_protect
def upload_file_view(request):
    prediction = None
    group = None
    error = None

    uploaded_files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        print("📂 Uploaded file:", uploaded_file)

        if uploaded_file:
            file_type = uploaded_file.content_type.split('/')[0]

            # Read the file *before* saving, or reset file pointer afterward
            try:
                file_data = uploaded_file.read().decode('utf-8')
                uploaded_file.seek(0)  # Reset stream after reading for storage

                UploadedFile.objects.create(
                    file=uploaded_file,
                    file_type=file_type,
                    user=request.user
                )

                reader = csv.DictReader(io.StringIO(file_data))
                record = next(reader)
                print("📄 Parsed CSV record:", record)
            except Exception as e:
                error = f"CSV error: {e}"
                print("❌ CSV Read Error:", e)
                return render(request, 'end_user_dashboard/enduserdash.html', {
                    'error': error,
                    'uploaded_files': uploaded_files
                })

            # Call prediction API
            try:
                response = requests.post('http://mlaas-service:9000/predict/', json=record)
                print("📡 Model response:", response.status_code, response.text)
                if response.status_code == 200:
                    data = response.json()
                    prediction = data.get('predicted_settlement')
                    group = data.get('cluster')
                else:
                    error = f"API Error: {response.status_code}"
            except Exception as e:
                error = f"Request failed: {e}"
                print("❌ Request Exception:", e)

    return render(request, 'end_user_dashboard/enduserdash.html', {
        'success': prediction is not None,
        'prediction': prediction,
        'group': group,
        'error': error,
        'uploaded_files': uploaded_files
    })

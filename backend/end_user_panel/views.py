from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm
from billing.utils import create_billing_record
import requests
import pandas as pd  # for file parsing
import os

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()

            # Get file path
            file_path = uploaded_file.file.path

            try:
                # Example: read a CSV and extract values for prediction
                df = pd.read_csv(file_path)
                wages = float(df.loc[0, 'wages'])
                medical = float(df.loc[0, 'medical'])

                # Prepare data for MLAAS
                payload = {"wages": wages, "medical": medical}
                response = requests.post("http://mlaas:9000/predict/", json=payload)

                if response.status_code != 200:
                    return JsonResponse({'error': 'Prediction failed'}, status=500)

                result = response.json().get("predicted_settlement")

                # Log billing
                if request.user.is_authenticated:
                    create_billing_record(request.user, "prediction", 0.50)

                return JsonResponse({
                    'message': 'Document uploaded and predicted successfully',
                    'predicted_settlement': result
                })

            except Exception as e:
                return JsonResponse({'error': f'Processing failed: {str(e)}'}, status=500)

    else:
        form = UploadFileForm()

    return render(request, 'end_user_panel/upload_file.html', {'form': form})

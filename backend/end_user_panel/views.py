import csv
import io
import requests
from django.shortcuts import render
from .models import UploadedFile
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def upload_file_view(request):
    prediction = None
    group = None
    error = None

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        print("📂 Uploaded file:", uploaded_file)
        if uploaded_file:
            file_type = uploaded_file.content_type.split('/')[0]
            UploadedFile.objects.create(file=uploaded_file, file_type=file_type)

            try:
                decoded_file = uploaded_file.read().decode('utf-8')
                reader = csv.DictReader(io.StringIO(decoded_file))
                record = next(reader)
                print("📄 Parsed CSV record:", record)
            except Exception as e:
                error = f"CSV error: {e}"
                print("❌ CSV Read Error:", e)

            try:
                response = requests.post('http://mlaas:9000/predict/', json=record)
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

            return render(request, 'end_user_panel/upload_file.html', {
                'success': True,
                'prediction': prediction,
                'group': group,
                'error': error
            })

    return render(request, 'end_user_panel/upload_file.html')

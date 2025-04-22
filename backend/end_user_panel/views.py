from django.shortcuts import render, redirect
from .models import UploadedFile
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def upload_file_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            file_type = uploaded_file.content_type.split('/')[0]
            UploadedFile.objects.create(file=uploaded_file, file_type=file_type)
            return render(request, 'end_user_panel/upload_file.html', {'success': True})
    return render(request, 'end_user_panel/upload_file.html')

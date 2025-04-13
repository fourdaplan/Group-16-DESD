
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Document uploaded successfully'})
    else:
        form = UploadFileForm()
    return render(request, 'end_user_panel/upload_file.html', {'form': form})

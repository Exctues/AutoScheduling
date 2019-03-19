from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from django.shortcuts import render
from u_csv.forms import DocumentForm
from django.shortcuts import redirect
from Backend import Data
from Backend.Common import nl
import os
from CATt import settings
import json

def model_form_upload(request):
    #form = DocumentForm()
    if request.method == 'POST':
        save_path = os.path.join(settings.BASE_DIR, 'files/')
        path = default_storage.save(save_path, request.FILES['file'])
        ans = Data.getScheduleData(path).split(nl)
        #data = json.dumps(ans)
        #return HttpResponse(data, content_type="application/json")
        return render(request, 'upload_form.html', { 'schedule': ans })
    else:
        #form = DocumentForm()
        return render(request, 'upload_form.html')


def print_csv_file(request):
    if request.method == 'POST':
        save_path = os.path.join(settings.BASE_DIR, 'files/')
        path = default_storage.save(save_path, request.FILES['file'])
        ans = Data.getScheduleData(path).split(nl)
        #data = json.dumps(ans)
        #return HttpResponse(data, content_type="application/json")
        return render(request, 'upload_form.html', { 'schedule': ans })
    else:
        redirect('')        


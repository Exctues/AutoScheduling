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
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('csv/')
    else:
        form = DocumentForm()
    return render(request, 'upload_form.html')


def print_csv_file(request):
    print(request.FILES)


    #save_path = os.path.join(settings.BASE_DIR, 'files/')
    #json.
    #save_path = os.path.join(save_path, request.FILES['file'])
    # path = os.path.join(settings.BASE_DIR, 'files/')
    path = 'Backend/Sample Data.csv'
    print(path)
    #path = default_storage.save(save_path, request.FILES['file'])
    ans = str(Data.getScheduleData(path)).split(nl)
    data = json.dumps(ans)
    #return HttpResponse()
    return HttpResponse(data, content_type="application/json")
    #return render(request, 'print_csv.html', { 'ans': ans })


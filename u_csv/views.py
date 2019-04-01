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
        return render(request, 'genSched.html', { 'schedule': ans })
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

def table_landing(request):
    a = list()
    a.append(["9:00", "10:30", "Networks Lecture"])
    a.append(["10:35", "12:05", "Networks Tutorial"])
    a.append(["12:10", "13:40", "Networks Lab"])
    return render(request, 'schedule.html', {
        'monday' : a
    })

def customized_view(request):
    if request.method == 'POST':
        gnumber = request.POST['Group']
        print("Group Number: gnumber", gnumber)
        ans = list()
        if gnumber == 1:
            ans.append(["9:00", "10:30", "Networks Lecture"])
            ans.append(["10:35", "12:05", "Networks Tutorial"])
            ans.append(["12:10", "13:40", "Networks Lab"])
        else:
            ans.append(["9:00", "10:30", "Lecture"])
            ans.append(["10:35", "12:05", "Tutorial"])
            ans.append(["12:10", "13:40", "Lab"])
        return render(request, 'schedule.html', {
            'monday' : ans
        })
    else:
        print("Request: ", request.GET)
        if request.GET:
            gnumber = request.GET['Group']
        else:
            gnumber = 1
        print("Group Number: gnumber", gnumber)
        ans = list()
        if gnumber == 1:
            ans.append(["9:00", "10:30", "Networks Lecture"])
            ans.append(["10:35", "12:05", "Networks Tutorial"])
            ans.append(["12:10", "13:40", "Networks Lab"])
        else:
            ans.append(["9:00", "10:30", "Lecture"])
            ans.append(["10:35", "12:05", "Tutorial"])
            ans.append(["12:10", "13:40", "Lab"])
        return render(request, 'schedule.html', {
            'monday' : ans
        })
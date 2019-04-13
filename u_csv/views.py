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
from schedule import ga
from schedule import data_process
def model_form_upload(request):
    if request.method == 'POST':
        save_path = os.path.join(settings.BASE_DIR, 'files/')
        path = default_storage.save(save_path, request.FILES['file'])
        # ans = Data.getScheduleData(path).split(nl)
        data = open(path)
        data2 = json.load(data)
        try:
            init = ga.GeneticSchedule.get_initial_population(data=data2, set_config=True)
        except:
            ans="Wrong input format"
            return render(request, 'genSched.html', { 'schedule': ans })
        sch = data_process.DataProcessor.denumerate_data(ga.GeneticSchedule.run(init))
        print(sch)
        ans="Everything is ok"
        return render(request, 'genSched.html', { 'schedule': ans })
    else:
        #form = DocumentForm()
        return render(request, 'upload_form.html')


def print_csv_file(request):
    if request.method == 'POST':
        save_path = os.path.join(settings.BASE_DIR, 'files/')
        path = default_storage.save(save_path, request.FILES['file'])
        ans = Data.getScheduleData(path).split(nl)
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
        if gnumber == '1':
            ans.append(["9:00", "10:30", "Networks Lecture"])
            ans.append(["10:35", "12:05", "Networks Tutorial"])
            ans.append(["12:10", "13:40", "Networks Lab"])
        else:
            ans.append(["9:00", "10:30", "Lecture"])
            ans.append(["10:35", "12:05", "Tutorial"])
            ans.append(["12:10", "13:40", "Lab"])
        print(ans)
        print("Something has happened")
        return render(request, 'schedule.html', {
            'monday' : ans
        })
    else:
        # print("Request: ", request.GET)
        if request.GET:
            gnumber = int(request.GET['Group'])
        else:
            gnumber = 1
        # print("Group Number: gnumber", gnumber)
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
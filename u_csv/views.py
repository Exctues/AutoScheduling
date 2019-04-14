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
from Backend import Schedule

table = []

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
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        times = ['09:00-10:30', '10:35-12:05', '12:10-13:40', '14:10-15:40', '15:45-17:15', '17:20-18:50', '18:55-20:25', '20:30-22:00']
        grades = dict()
        grades['BS17'] = ['BS17-0' + str(i) for i in range(1, 9)]
        grades['BS18'] = ['BS18-0' + str(i) for i in range(1, 9)]
        grades['B16-DS'] = ['B16-DS-01']

        
        table = Schedule.Schedule(days, times, grades, list(), list(), list())
        json_path = os.path.join(settings.BASE_DIR, 'Backend/')
        json_path = json_path + 'sample.json'
        # print("json_path = ", json_path)
        try:
            Schedule.AddAlgoOutputToDS(json_path, table)
        except Schedule.JSONException as e:
            print(e)
            return HttpResponse()
        
        grades = table.getGrades()
        groups = []
        for x in grades:
            for y in table.getGroupsOfGrade(x):
                groups.append(y)

        if request.GET:
            course = request.GET['Course']
            gnumber = request.GET['Group']
        else:
            gnumber = groups[0]
            course = 'Course'
        
        print("Group Number: gnumber", gnumber, course)
        ans = list()
        slots = table.getSlotsOfGroup(gnumber)
        monday = list()
        tuesday = list()
        wednesday = list()
        thursday = list()
        friday = list()
        saturday = list()
        for s in slots:
            if s.getDay() == 'Monday':
                ts, tf = s.getTime().split('-')
                label = s.getLabel()
                monday.append([ts, tf, label])
            if s.getDay() == 'Tuesday':
                ts, tf = s.getTime().split('-')
                label = s.getLabel()
                tuesday.append([ts, tf, label])
            if s.getDay() == 'Wednesday':
                ts, tf = s.getTime().split('-')
                label = s.getLabel()
                wednesday.append([ts, tf, label])
            if s.getDay() == 'Thursday':
                ts, tf = s.getTime().split('-')
                label = s.getLabel()
                thursday.append([ts, tf, label])
            if s.getDay() == 'Friday':
                ts, tf = s.getTime().split('-')
                label = s.getLabel()
                friday.append([ts, tf, label])
            if s.getDay() == 'Saturday':
                ts, tf = s.getTime().split('-')
                label = s.getLabel()
                saturday.append([ts, tf, label])
        print("monday=", monday)
        ans.append(["9:00", "10:30", "Networks Lecture"])
        ans.append(["10:35", "12:05", "Networks Tutorial"])
        ans.append(["12:10", "13:40", "Networks Lab"])
        for s in slots:
            print(s)
        return render(request, 'schedule.html', {
            'groups' : groups,
            'grades' : grades,
            'monday' : monday,
            'tuesday' : tuesday,
            'wednesday' : wednesday,
            'thursday' : thursday,
            'friday' : friday,
            'saturday' : saturday
        })
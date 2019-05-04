import pandas as pd
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Parsers.Schedule import JSONException
from Parsers.CSVParser import CSVException, CreateDSAndJSON
import os
from site.CATt import settings
from gscript import run_gscript
import json
from schedule import data_exchange, call_scheduler
from .models import UploadedCSV
from .models import GeneratedSchedules
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from schedule.data_exchange import Exchanger
from threading import Thread


class GeneratorThread(Thread):
    def __init__(self, request, schnum, max_execution_time, generated_schedule):
        Thread.__init__(self)
        self.request = request
        self.schnum = schnum
        self.max_execution_time = max_execution_time
        self.generated_schedule = generated_schedule

    def run(self, ):
        print("schedule number = ", self.schnum)
        csv_list = UploadedCSV.objects.get(id=self.schnum)
        path_to_csv = str(csv_list.file_location)
        path_to_json = os.path.join(settings.BASE_DIR, 'files/')
        path_to_json = path_to_json + 'input.json'
        cwd = os.path.dirname(os.path.abspath(__file__))

        try:
            number = GeneratedSchedules.objects.latest('id').id + 1
        except Exception:
            number = 1

        try:
            CreateDSAndJSON(path_to_csv, path_to_json)
        except CSVException as e:
            print(f"Wrong input format\n{e}")

        try:
            data_exchange.Exchanger.json_to_cfg(path_to_json, cwd + f"/../../scheduler_cpp/files/Schedule_{number}.cfg")
        except Exception:
            print('error')
            self.generated_schedule.status = "Error"
            self.generated_schedule.save()
            return
        try:
            sch = call_scheduler.run(cwd + f"/../../scheduler_cpp/files/Schedule_{number}.cfg")
        except Exception as e:
            print(f"Internal error, error message: {e}")
            self.generated_schedule.status = "Error"
            return
        path = os.path.join(settings.BASE_DIR, 'files/')

        file_name = f'user_{str(self.request.user.id)}_schedule{str(number)}.json'
        path = path + file_name
        sch = json.loads(sch)

        # =====
        js = sch
        df = pd.DataFrame(js)
        grouped_schedule = df.groupby(by=['Auditorium', 'Day', 'Time']).groups
        new_js = []

        for key, ids in grouped_schedule.items():
            if len(ids) == 1:
                item = df.loc[ids[0]].to_dict()
            else:
                item = df.loc[ids]
                groups = item.Group
                while len(groups) > 1:
                    groups = list(set(["-".join(group.split('-')[:-1]) for group in groups]))
                item = item.iloc[0]
                item.Group = groups[0]
                item = item.to_dict()
            new_js.append(item)
        # ====

        with open(path, 'w') as json_file:
            json.dump(new_js, json_file)

        spreadsheet = run_gscript('files/' + file_name)
        spreadsheet = None if spreadsheet[0] == '!' else spreadsheet

        self.generated_schedule.location = path
        self.generated_schedule.google_sheet = spreadsheet
        self.generated_schedule.used_csv_files = path_to_csv
        self.generated_schedule.status = "Done"
        self.generated_schedule.save()


@login_required(login_url='/login/')
def model_form_upload(request):
    global table
    if request.method == 'POST':
        save_path = os.path.join(settings.BASE_DIR, 'files/')
        if not request.FILES:
            ans = "choose file"
            return render(request, 'upload_form.html', {'message': ans})

        path = default_storage.save(save_path, request.FILES['file'])
        csv_upload = UploadedCSV()
        csv_upload.original_file_name = request.FILES['file']
        csv_upload.file_location = path
        csv_upload.user = request.user
        csv_upload.save()
        return HttpResponseRedirect('/upload/uploaded')
    else:
        print("request received = ", request.GET)
        path = os.path.join(settings.BASE_DIR, 'files/')
        path = path + 'schedule.json'
        print("removing")
        try:
            os.remove(path)
        except:
            print("cant remove schedule.json")

        return render(request, 'upload_form.html')


@login_required(login_url='/login/')
def schedule_generate(request, schnum, time):
    try:
        UploadedCSV.objects.get(id=schnum)
    except:
        return HttpResponse(status=400, content='Error: not exists')
    generated_schedule = GeneratedSchedules()
    generated_schedule.user = request.user
    generated_schedule.status = "Pending"
    generated_schedule.save()

    generation_thread = GeneratorThread(request=request, schnum=schnum, max_execution_time=time * 60,
                                        generated_schedule=generated_schedule)
    generation_thread.start()
    return HttpResponseRedirect('/upload/history')


@login_required(login_url='/login/')
def scheduleHistory(request):
    schedulelist = GeneratedSchedules.objects.filter(user=request.user.id).order_by("-date_generated")
    return render(request, 'history.html', {
        'schItems': schedulelist
    })


@login_required(login_url='/login/')
def uploadedHisotry(request):
    somelist = UploadedCSV.objects.filter(user=request.user)
    return render(request, 'uploaded.html', {
        'hItems': somelist
    })


@login_required(login_url='/login/')
@csrf_exempt
def edit_schedule(request, number):
    if request.method == "GET":
        try:
            schedule = GeneratedSchedules.objects.get(id=number)
            if schedule.user != request.user:
                raise IndexError
        except:
            return HttpResponse(status=400, content='Incorrect schedule number')
        sch = json.load(open(schedule.location, 'r'))
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        auditoriums = set([less['Auditorium'] for less in sch])
        times_slot = set([less['Time'] for less in sch])
        sch.sort(key=lambda lesson: lesson["Course_name"])
        return render(request, 'edit_schedule.html',
                      {'Schedule_Number': number, 'schedule': sch, 'days': days, 'auditoriums': auditoriums,
                       'times': times_slot})
    elif request.method == "POST":
        try:
            schedule_raw = json.loads(request.body)["schedule"]
            schedule = GeneratedSchedules.objects.get(id=number)
            if schedule.user != request.user:
                raise IndexError
        except:
            return HttpResponse('provide correct input values', status=400)
        exception_str = check_correctness(schedule_raw)

        if exception_str is not None:
            return HttpResponse(content=exception_str, status=400)
        sch = GeneratedSchedules()
        sch.location = f'files/{str(request.user.id)}_temp_schedule_{str(number)}'

        sch.user = request.user
        sch.used_csv_files = schedule.used_csv_files
        sch.status = "TEMP"
        with open(sch.location, 'w') as f:
            f.write(json.dumps(schedule_raw))
        sch.save()
        return HttpResponse(f'schedule/{sch.id}/')


@login_required(login_url='/login/')
@csrf_exempt
def save_schedule(request, number):
    if request.method == "POST":
        try:
            schedule_raw = json.loads(request.body)["schedule"]
            schedule = GeneratedSchedules.objects.get(id=number)
            if schedule.user != request.user:
                raise IndexError
        except:
            return HttpResponse('provide correct input values', status=400)
        exception_str = check_correctness(schedule_raw)
        if exception_str is not None:
            return HttpResponse(content=exception_str, status=400)
        with open(schedule.location, 'w') as f:
            f.write(json.dumps(schedule_raw))
        run_gscript(schedule.location, update=True, url=schedule.google_sheet)
        return HttpResponse('Successfully saved')


def check_correctness(sch):
    lesson_str = lambda lesson1, lesson2: f'''{lesson1['Course_name'] + ' ' + lesson1['Lesson_type']} & {lesson2[
                                                                                                             'Course_name'] + ' ' +
                                                                                                         lesson2[
                                                                                                             'Lesson_type']}'''
    for lesson1 in sch:
        for lesson2 in sch:
            if lesson1 != lesson2:
                eq_time = lesson1['Time'] == lesson2['Time'] and lesson1['Day'] == lesson2['Day']
                slot = f'''{lesson1['Day']} {lesson1['Time']}'''
                if eq_time:
                    if lesson1['Group'] == lesson2['Group']:
                        return f'''Group {lesson1['Group']} has two lessons per same time slot ({slot})
                        {lesson_str(lesson1, lesson2)}'''
                    if lesson1['Auditorium'] == lesson2['Auditorium']:
                        return f'''In Auditorium {lesson1[
                            'Auditorium']} two different lessons are going per same time slot ({slot}) - {lesson_str(
                            lesson1,
                            lesson2)}'''
                    if lesson1['Faculty'] == lesson2['Faculty']:
                        return f'''{lesson1[
                            'Faculty']} has two different lessons in same time slot ({slot})- {lesson_str(
                            lesson1, lesson2)}'''
    return None


@login_required(login_url='/login/')
@csrf_exempt
def downloadSchedule(request, number):
    try:
        sch = GeneratedSchedules.objects.filter(id=number)[0]
    except:
        return HttpResponseRedirect('/upload/')
    ftemp = f'files/{str(request.user.id)}_{str(number)}'
    # a little bit unefficient
    Exchanger.json_to_csv(sch.location, ftemp)
    data = ''.join(i for i in open(ftemp, 'r'))
    file_to_send = ContentFile(data)
    response = HttpResponse(file_to_send, 'application/csv')
    response['Content-Length'] = file_to_send.size
    response['Content-Disposition'] = 'attachment; filename="schedule.csv"'
    os.remove(ftemp)
    return response


@login_required(login_url='/login/')
def downloadUploadedCsv(request, number):
    try:
        sch = UploadedCSV.objects.filter(id=number)[0]
        if sch.user != request.user:
            return HttpResponse(status=400, content='Provide values')
    except:
        return HttpResponseRedirect('/upload/')
    data = ''.join(i for i in sch.file_location.open('r'))
    file_to_send = ContentFile(data)
    response = HttpResponse(file_to_send, 'application/csv')
    response['Content-Length'] = file_to_send.size
    response['Content-Disposition'] = 'attachment; filename="schedule.csv"'
    return response


@login_required(login_url='/login/')
def show_schedule_view(request, number):
    if request.method == 'POST':
        ans = ''
        return render(request, 'schedule.html', {
            'monday': ans,
        })
    else:
        try:
            schedule = GeneratedSchedules.objects.get(id=number)
            if schedule.user != request.user:
                raise IndexError
        except:
            return HttpResponse('incorrect schedule number', status=400)
        path_to_csv = schedule.used_csv_files
        path_to_json = os.path.join(settings.BASE_DIR, 'files/')
        path_to_json = path_to_json + 'input.json'
        try:
            table = CreateDSAndJSON(path_to_csv, path_to_json)
        except CSVException as e:
            return HttpResponse(str(e))
        json_path = schedule.location
        try:
            table.addDataFromJSON(json_path)
        except JSONException:
            return HttpResponse('An internal error occurred')
        if schedule.status == 'TEMP':
            try:
                os.remove(schedule.location)
            except:
                pass
            schedule.delete()
        return render_schedule(request, table, glink=schedule.google_sheet)


def render_schedule(request, table, glink=''):
    grades = table.getGrades()
    groups = []
    for x in grades:
        for y in table.getGroupsOfGrade(x):
            groups.append(y)

    gradelist = [k for k in grades]
    if request.GET:
        course = request.GET['Course']
        gnumber = request.GET['Group']
    else:
        gnumber = groups[0]
        course = gradelist[0]

    groups.remove(gnumber)
    groups = [gnumber] + groups
    gradelist.remove(course)
    gradelist = [course] + gradelist
    slots = table.getSlotsOfGroup(gnumber)
    monday = list()
    tuesday = list()
    wednesday = list()
    thursday = list()
    friday = list()
    saturday = list()
    res = {'Monday': monday, 'Tuesday': tuesday, 'Wednesday': wednesday, 'Thursday': thursday, 'Friday': friday}
    for s in slots:
        if s.getDay() not in res:
            continue
        result = res[s.getDay()]
        ts, tf = s.getTime().split('-')
        label = s.getLabel()
        result.append([ts, tf, label])
    return render(request, 'schedule.html', {
        'groups': groups,
        'grades': gradelist,
        'monday': monday,
        'tuesday': tuesday,
        'wednesday': wednesday,
        'thursday': thursday,
        'friday': friday,
        'saturday': saturday,
        'gsheet_link': glink
    })

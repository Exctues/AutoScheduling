from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import json
from user_profile.models import UserProfile
from django.http import HttpResponseRedirect


@csrf_exempt
def loginView(request):

    if request.method == 'GET':
        return render(request=request, template_name='login.html')
    elif request.method == 'POST':
        try:
            json_data = json.loads(request.body)  #
            username = json_data['username']
            password = json_data['password']
        except:
            return HttpResponse(content='Provide values', status=400)
        user = User.objects.filter(username=username, password=password)
        if user.count() == 0:
            return HttpResponse(content='Invalid credentials', status=400)
        else:
            login(request, user[0])
            return HttpResponse(status=200)


@csrf_exempt
def registerView(request):
    if request.method == 'GET':
        return render(request=request, template_name='register.html')
    elif request.method == 'POST':
        try:
            json_data = json.loads(request.body)  #
            email = json_data['email']
            name = json_data['username']
            password = json_data['password']
        except:
            return HttpResponse(content='Provide values', status=400)
        if UserProfile.objects.filter(username=email).count() > 0:
            return HttpResponse(content='Provide correct values', status=400)
        user = UserProfile(username=email, first_name=name, password=password)
        user.save()
        return HttpResponseRedirect('/login/')


@login_required(login_url='/login/')
def logoutView(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect('/login/')

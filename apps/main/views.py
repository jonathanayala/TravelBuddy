from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Count
from django.db import models
from .models import User, Travel


def index(request):
    return render(request, 'main/index.html')

def registration(request):
    if request.method == 'GET':
        return redirect ('index')
    new_user = User.objects.validate(request.POST)
    if new_user[0] == True:
        request.session['id'] = new_user[1].id
        return redirect('travel')
    if new_user[0] == False:
        for each in new_user[1]:
            messages.error(request, each)
        return redirect('index')

def login(request):
    if request.method == 'GET':
        return redirect('index')
    if 'id' in request.session:
        return redirect('travel')
    else:
        user = User.objects.login(request.POST)
        if user[0] == True:
            messages.add_message(request, messages.INFO,'You logged in!')
            request.session['id'] = user[1].id
            return redirect('travel')
        if user[0] == False:
            for each in user[1]:
                messages.add_message(request, messages.INFO, each)
            return redirect('index')

def logout(request):
    if 'id' not in request.session:
        return redirect('index')
    del request.session['id']
    return redirect('index')

def travel(request):
    if 'id' not in request.session:
        return redirect ("index")
    context = {
        "user": User.objects.get(id=request.session['id']),
        "travels" : Travel.objects.all(),
        "others": Travel.objects.all().exclude(join__id=request.session['id'])
    }
    return render(request, 'main/travels.html', context)

def add_plan(request):
    if 'id' not in request.session:
        return redirect ("index")
    else:
        context= {
            "user": User.objects.get(id=request.session['id']),
        }
        return render(request, 'main/add.html', context)

def create_plan(request):
    if request.method != 'POST':
        return redirect ("add_plan")
    new_plan= Travel.objects.travelvalidate(request.POST, request.session["id"])
    if new_plan[0] == True:
        return redirect('travel')
    else:
        for message in new_plan[1]:
            messages.error(request, message)
        return redirect('add_plan')

def show(request, travel_id):
    try:
        travel = Travel.objects.get(id=travel_id)
    except Travel.DoesNotExist:
        messages.info(request, "Travel Not Found")
        return redirect('travel')
    context = {
        "travel": travel,
        "user": User.objects.get(id=request.session['id']),
        "others": User.objects.filter(joiner__id=travel.id).exclude(id=travel.creator.id)
    }
    return render(request, 'main/destination.html', context)

def join(request, travel_id):
    if request.method == "GET":
        messages.error(request,"What trip you want to join?")
        return redirect('index')
    joiner= Travel.objects.join(request.session["id"], travel_id)
    if 'errors' in joiner:
        messages.error(request, joiner['errors'])
    return redirect('travel')
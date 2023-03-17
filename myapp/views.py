from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
import json


def classes(request):
    url = 'https://api.devhub.virginia.edu/v1/courses'
    data = requests.get(url).json()
    records = data['class_schedules']['records']
    headers = data['class_schedules']['columns']
    return render(request, 'classes.html', {'records': records, 'headers': headers})


def login(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'template.html', {})


@login_required
def home(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'tutor':
            return redirect('tutor-home')
        elif role == 'student':
            return redirect('student-home')
    else:
        return render(request, 'home.html')


def student_home(request):
    return render(request, 'student_home.html')


def tutor_home(request):
    return render(request, 'tutor_home.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from myapp.models import Course
from django.db.models import Q


def fetch_courses(page_size=100):
    url = 'https://api.devhub.virginia.edu/v1/courses'
    courses = []

    page_num = 1
    while True:
        params = {
            'page': page_num,
            'page_size': page_size
        }
        response = requests.get(url, params=params)
        data = response.json()
        records = data['class_schedules']['records']
        
        if not records:
            break
        
        for record in records:
            course = Course(
                subject=record[0],
                catalog_number=record[1],
                class_section=record[2],
                class_number=record[3],
                class_title=record[4],
                class_topic_formal_desc=record[5],
                instructor=record[6],
                enrollment_capacity=record[7],
                meeting_days=record[8],
                meeting_time_start=record[9],
                meeting_time_end=record[10],
                term=record[11],
                term_desc=record[12]
            )
            courses.append(course)

        page_num += 1
    
    Course.objects.bulk_create(courses)

    return courses

def course_list(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(Q(class_title__icontains=query) | Q(class_number__icontains=query))
    else:
        courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


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

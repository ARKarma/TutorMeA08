from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from myapp.models import Course
from django.db.models import Q


def fetch_courses():
    url = 'https://api.devhub.virginia.edu/v1/courses'
    data = requests.get(url).json()

    courses = []
    for record in data['class_schedules']['records']:
        course = Course(
            subject=record[0],
            catalog_number=record[1],
            sub_and_cat =record[0] + " " + record[1],
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
        course.save()  # save the course instance to the database
        courses.append(course)

    print(f"Fetched {len(courses)} courses")
    return courses


def course_list(request):
    # if not Course.objects.all():
    #     fetch_courses()
    
    query = request.GET.get('q')
    print(query)
    if query:
        courses = Course.objects.filter(Q(sub_and_cat__icontains=query) | Q(subject__icontains=query) | Q(catalog_number__icontains=query) | Q(class_title__icontains=query) | Q(class_number__icontains=query))
        #courses = Course.objects.filter(Q(subject__icontains=query) | Q(catalog_number__icontains=query) | Q(sub_and_cat__icontains=query)) #| Q(class_title__icontains=query) | Q(class_number__icontains=query))
    else:
        courses = Course.objects.all()
    print(courses)
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

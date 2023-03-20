from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from myapp.models import Course
from django.db.models import Q

def fetch_courses():
    #courses = []
    url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&acad_career=UGRD'
    
    for x in range(5,10):
        data = requests.get(url + '&page=' + str(x))
        for c in data.json():
            course = Course(
                subject= c['subject'],
                catalog_number=c['catalog_nbr'],
                sub_and_cat=c['subject']+ " " + c['catalog_nbr'],
                class_section=c['class_section'],
                class_number=c['class_nbr'],
                class_title=c['descr'],
                #class_topic_formal_desc=record[5],
                instructor=c['instructors'],
                #enrollment_capacity=record[7],
                #meeting_days=record[8],
                #meeting_time_start=record[9],
                #meeting_time_end=record[10],
                #term=record[11],
                #term_desc=record[12]
            )
            course.save()  # save the course instance to the database
            #courses.append(course)

    #print(f"Fetched {len(courses)} courses")
    return

def course_list(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(Q(sub_and_cat__icontains=query) | Q(subject__icontains=query) | Q(catalog_number__icontains=query) | Q(class_title__icontains=query) | Q(class_number__icontains=query))
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

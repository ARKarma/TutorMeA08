from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from myapp.models import User


def login(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'template.html', {})


@login_required
def home(request):
    logged_in_user = request.user
    email = logged_in_user.email
    try:
        current_user = User.objects.get(pk=email)
    except User.DoesNotExist:
        if request.method == 'POST':
            role = request.POST.get('role')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            if role == 'tutor':
                new_user = User(email=email, first_name=first_name,
                                last_name=last_name, user_role=User.TUTOR)
                new_user.save()
                return redirect('tutor-home')
            elif role == 'student':
                new_user = User(email=email, first_name=first_name,
                                last_name=last_name, user_role=User.STUDENT)
                new_user.save()
                return redirect('student-home')
        else:
            return render(request, 'home.html')

    if(current_user != None):
        if(current_user.user_role == User.STUDENT):
            return redirect('student-home')
        elif(current_user.user_role == User.TUTOR):
            return redirect('tutor-home')


def student_home(request):
    return render(request, 'student_home.html')


def tutor_home(request):
    return render(request, 'tutor_home.html')

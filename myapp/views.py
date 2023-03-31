from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from myapp.models import Course
from myapp.models import Session
from myapp.models import Course, User
from django.db.models import Q
from myapp.forms import SessionForm
from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404

def fetch_courses():
    # courses = []
    url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&acad_career=UGRD'

    for x in range(1, 3):
        data = requests.get(url + '&page=' + str(x))
        for c in data.json():
            if Course.objects.filter(sub_and_cat__icontains=c['subject'] + " " + c['catalog_nbr']):
                pass
            else:
                course = Course(
                    subject=c['subject'],
                    catalog_number=c['catalog_nbr'],
                    sub_and_cat=c['subject'] + " " + c['catalog_nbr'],
                    class_section=c['class_section'],
                    class_number=c['class_nbr'],
                    class_title=c['descr'],
                    instructor=c['instructors'],
                )
                course.save()  # save the course instance to the database
            # courses.append(course)

    # print(f"Fetched {len(courses)} courses")
    return


def course_list(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(
            Q(sub_and_cat__icontains=query) | Q(subject__icontains=query) | Q(catalog_number__icontains=query) | Q(
                class_title__icontains=query))
    else:
        courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def view_sessions(request, pk):
      course = Course.objects.get(pk=pk)
      sessions = Session.objects.filter(class_title=pk)
      return render(request, 'course_session_view.html', {'course': course}, {'sessions': sessions})


# class SessionsView(generic.DetailView):
#     # model = Session

#     template_name = 'course_session_view.html'

#     def get_queryset(self):
#         self.course = get_object_or_404(Course, name=self.kwargs['course'])
#         return Session.objects.filter(class_title=self.course)
    
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in the publisher
#         context['course'] = self.course
#         return context
    # course = 
    # template_name = 'course_session_view.html'
    

    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     return Session.objects.filter(class_title=sub_and_cat)


def login(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'template.html', {})


@login_required
def home(request):
	logged_in_user = request.user
	email= logged_in_user.email
	try:
		current_user = User.objects.get(pk=email)
	except User.DoesNotExist:
		if request.method == 'POST':
			role = request.POST.get('role')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			if role == 'tutor':
				new_user = User(email=email, first_name=first_name, last_name=last_name, user_role=User.TUTOR)
				new_user.save()
				return redirect('tutor-home')
			elif role == 'student':
				new_user = User(email=email, first_name=first_name, last_name=last_name, user_role=User.STUDENT)
				new_user.save()
				return redirect('student-home')
		else:
			return render(request, 'home.html')

	if(current_user!=None):
		if(current_user.user_role==User.STUDENT):
			return redirect('student-home')
		elif(current_user.user_role==User.TUTOR):
			return redirect('tutor-home')


def student_home(request):
    return render(request, 'student_home.html')


def tutor_home(request):
    return render(request, 'tutor_home.html')


def post_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.tutor = request.user
            session.save()
            messages.success(request, 'Session posted successfully.')
            return redirect('tutor-home')
    else:
        form = SessionForm()

    return render(request, 'post_session.html', {'form': form})

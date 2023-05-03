from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from myapp.models import *
from django.db.models import Q
from myapp.forms import *
from django.views import generic
from django.shortcuts import get_object_or_404, Http404
from myapp.forms import BookingForm
from datetime import datetime, date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
import calendar
from .utils import Calendar
from django.utils.safestring import mark_safe
from .models import Profile


def fetch_courses():
    # courses = []
    url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&acad_career=UGRD'

    for x in range(40, 44):
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


@login_required
def course_list(request):
    subject_query = request.GET.get('sub')
    catalog_query = request.GET.get('cat')
    title_query = request.GET.get('course_title')
    courses = Course.objects.all()
    logged_in_user = request.user
    email = logged_in_user.email
    try:
        current_user = AppUser.objects.get(pk=email)
    except AppUser.DoesNotExist:
        return redirect('login.html')
    if subject_query:
        subject_list = courses.filter(Q(subject__icontains=subject_query))
        courses = subject_list
    if catalog_query:
        catalog_list = courses.filter(
            Q(catalog_number__icontains=catalog_query))
        courses = catalog_list
    if title_query:
        title_list = courses.filter(Q(class_title__icontains=title_query))
        courses = title_list
    if (not subject_query) & (not catalog_query) & (not title_query):
        courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses, 'cur_User': current_user})


@login_required
def view_sessions(request, pk):
    course = get_object_or_404(Course, pk=pk)
    sessions = Session.objects.filter(course=course)
    logged_in_user = request.user
    if logged_in_user.is_anonymous:
        return redirect('/login/')
    try:
        email = logged_in_user.email
        current_user = AppUser.objects.get(pk=email)
        return render(request, 'course_session_view.html',
                      {'sessions': sessions, 'course': course, 'cur_User': current_user})
    except AppUser.DoesNotExist:
        return redirect("login.html")
    return render(request, 'course_session_view.html', {'sessions': sessions, 'course': course})


def login(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'template.html', {})


@login_required
def home(request):
    logged_in_user = request.user
    email = logged_in_user.email
    try:
        current_user = AppUser.objects.get(pk=email)
    except AppUser.DoesNotExist:
        if request.method == 'POST':
            role = request.POST.get('role')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            if role == 'tutor':
                new_user = AppUser(email=email, first_name=first_name,
                                   last_name=last_name, user_role=AppUser.TUTOR)
                new_user.save()
                return redirect('tutor-home')
            elif role == 'student':
                new_user = AppUser(email=email, first_name=first_name,
                                   last_name=last_name, user_role=AppUser.STUDENT)
                new_user.save()
                return redirect('student-home')
        else:
            return render(request, 'home.html')

    if current_user is not None:
        if current_user.user_role == AppUser.STUDENT:
            return redirect('student-home')
        elif current_user.user_role == AppUser.TUTOR:
            return redirect('tutor-home')


@login_required
def student_home(request):
    logged_in_user = request.user
    email = logged_in_user.email
    try:
        current_user = AppUser.objects.get(pk=email)
        if (current_user.user_role == AppUser.TUTOR):
            return redirect('tutor_home.html')
    except AppUser.DoesNotExist:
        return redirect('login.html')
    try:
        bookings = Booking.objects.filter(user=logged_in_user)
    except Booking.DoesNotExist:
        bookings = None
    return render(request, 'student_home.html', {'cur_User': current_user, 'bookings': bookings})


@login_required
def tutor_home(request):
    logged_in_user = request.user
    email = logged_in_user.email
    try:
        current_user = AppUser.objects.get(pk=email)
        if (current_user.user_role == AppUser.STUDENT):
            return redirect('student_home.html')
    except AppUser.DoesNotExist:
        return redirect('login.html')
    try:
        cur_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return render(request, 'tutor_home.html', {'cur_User': current_user, 'no_Profile': True})
    if (request.method == 'POST'):
        cur_bookingid = request.POST.get('cur_booking')
        cur_booking = Booking.objects.get(pk=cur_bookingid)
        appointment_selection = request.POST.get('decision')
        if (appointment_selection == "accept"):
            cur_booking.booking_status = Booking.ACCEPTED
        elif (appointment_selection == "reject"):
            cur_booking.booking_status = Booking.DECLINED
        cur_booking.save()

    try:
        sessions = Session.objects.filter(tutor=logged_in_user)
    except Session.DoesNotExist:
        sessions = None
    bookings = []
    for session in sessions:
        # Will need to make a check so that you can only have one booking per session
        try:
            bookingl = Booking.objects.filter(session=session)
        except Booking.DoesNotExist:
            bookingl = None
        if (bookingl != None):
            for booking in bookingl:
                bookings.append(booking)

    my_param = request.GET.get('my_param')
    context = {'my_param': my_param,
               'cur_User': current_user,
               'no_Profile': False,
               'bookings': bookings,
               }

    return render(request, 'tutor_home.html', context)


@login_required
def current_appointments(request):
    logged_in_user = request.user
    email = logged_in_user.email
    try:
        current_user = AppUser.objects.get(pk=email)
    except AppUser.DoesNotExist:
        # Prob a better way to ensure safety; let's implement later
        return render(request, 'current_appointments.html')
    # Get all bookings
    try:
        bookings = Booking.objects.filter(user=logged_in_user)
    except Booking.DoesNotExist:
        bookings = None

    return render(request, 'current_appointments.html', {'cur_User': current_user, 'bookings': bookings})


@login_required
def post_session(request):

    try:
        cur_profile = Profile.objects.get(user=request.user)
        coursesQuery = cur_profile.qualified_courses.all()
    except Profile.DoesNotExist:
        return redirect('tutor-home')
    try:
        current_user = AppUser.objects.get(pk=request.user.email)
    except AppUser.DoesNotExist:
        return redirect('login.html')
    if request.method == 'POST':
        req = request.POST
        courses = req.getlist('courses[]')

        for course in courses:
            cour = Course.objects.get(sub_and_cat=course)
            dt = req.get('date')
            st = req.get('start_time')
            et = req.get('end_time')
            today = date.today()

            if dt < str(today) or st >= et:
                date_error = False
                time_error = False
                if dt < str(today):
                    date_error = True
                if st >= et:
                    time_error = True

                context = {
                    'coursesQuery': coursesQuery,
                    'date_error': date_error,
                    'time_error': time_error,
                }
                return render(request, 'post_session.html', context)

            session = Session(tutor=request.user, course=cour, description=req.get('description'),
                              price=req.get('price'), date=req.get('date'), start_time=req.get('start_time'),
                              end_time=req.get('end_time'))
            session.save()

            messages.success(
                request, 'Session posted successfully.', fail_silently=True)

        my_param = "session_success"
        return redirect('/tutor-home/?my_param={}'.format(my_param))
    return render(request, 'post_session.html', {'coursesQuery': coursesQuery, 'cur_User': current_user})


@login_required
def book_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.session = session
            booking.user = request.user._wrapped if hasattr(
                request.user, '_wrapped') else request.user
            booking.save()
            messages.success(request, 'Session booked successfully!')

            # Render the booking confirmation template
            return render(request, 'booking_confirmation.html', {'booking': booking})
    else:
        form = BookingForm()

    return render(request, 'book_session.html', {'form': form, 'session': session})


@login_required
def booking_confirmation(request, course_id):
    if request.method == 'POST':
        return redirect('course_list')
    return render(request, 'booking_confirmation.html', {'course_id': course_id})


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            current_user = AppUser.objects.get(pk=self.request.user.email)
        except AppUser.DoesNotExist:
            current_user = None
        # use today's month for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date, and the current user
        cal = Calendar(d.year, d.month, self.request.user)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['cur_User'] = current_user
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required
def profile(request):
    # Make profile if it doesn't exist
    courses = Course.objects.all()
    try:
        cur_profile = Profile.objects.get(user=request.user)
        cur_User = AppUser.objects.get(pk=request.user.email)
    except Profile.DoesNotExist:
        cur_User = AppUser.objects.get(pk=request.user.email)
        cur_profile = Profile(
            appUser=cur_User, user=request.user, about_me="Describe yourself")
        cur_profile.save()
    if request.method == 'POST':
        form = request.POST
        cur_profile.about_me = form.get('about')
        cur_profile.qualified_courses.set(form.getlist('courses[]'))
        cur_profile.save()
        my_param = "profile_success"
        return redirect('/tutor-home/?my_param={}'.format(my_param))
    try:
        coursesQuery = cur_profile.qualified_courses.all()
    except:
        coursesQuery = None
    return render(request, 'profile.html', {'cur_User': cur_User, 'courses': courses, 'curProfile': cur_profile, 'coursesQuery': coursesQuery})


def tutor_profile(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
        user = profile.user
        print(profile.qualified_courses.all())
    except Profile.DoesNotExist:
        raise Http404("Tutor profile does not exist")
    return render(request, 'tutor_profile.html', {'user': user, 'profile': profile})


def chat(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    messages = MessageChat.objects.filter(sender=request.user, receiver=receiver) | MessageChat.objects.filter(
        sender=receiver, receiver=request.user)
    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        message = MessageChat(sender=request.user,
                              receiver=receiver, content=content)
        message.save()
        return redirect('chat', receiver_id=receiver_id)

    return render(request, 'chat.html', {'receiver': receiver, 'messages': messages})


def start_chat(request, user_id):
    if request.user.is_authenticated:
        app_user = AppUser.objects.get(email=request.user.email)
        target_user = User.objects.get(id=user_id)

        if app_user.is_student_true:
            # If the authenticated user is a student, the target user is the tutor
            tutor = target_user
        else:
            # If the authenticated user is a tutor, the target user is the student
            tutor = request.user
            target_user = User.objects.get(id=user_id)

        # Pass the target user's ID as the receiver_id
        return redirect('chat', receiver_id=target_user.id)
    else:
        return redirect('login')


@login_required
def tutor_chats(request):
    logged_in_user = request.user
    email = logged_in_user.email
    try:
        current_user = AppUser.objects.get(pk=email)
        if current_user.user_role != AppUser.TUTOR:
            return redirect('student_home')
    except AppUser.DoesNotExist:
        return redirect('login.html')

    chats = MessageChat.objects.filter(
        receiver=request.user).values('sender').distinct()
    chats_list = [User.objects.get(id=chat['sender']) for chat in chats]

    return render(request, 'tutor_chats.html', {'chats': chats_list})


@login_required
def student_chats(request):
    logged_in_user = request.user
    email = logged_in_user.email
    try:
        current_user = AppUser.objects.get(pk=email)
        if current_user.user_role != AppUser.STUDENT:
            return redirect('tutor_home')
    except AppUser.DoesNotExist:
        return redirect('login.html')

    chats = MessageChat.objects.filter(
        sender=request.user).values('receiver').distinct()
    chats_list = [User.objects.get(id=chat['receiver']) for chat in chats]

    return render(request, 'student_chats.html', {'chats': chats_list})

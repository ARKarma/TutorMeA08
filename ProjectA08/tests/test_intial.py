import pytest
from django.urls import reverse
from myapp.views import *
from django.contrib.auth.models import AnonymousUser, User, AbstractBaseUser, UserManager
from django.contrib.messages import *
from django.test import RequestFactory
from myapp.models import Course, AppUser
from unittest.mock import Mock, MagicMock, patch
import sqlite3

@pytest.mark.django_db
def test_1_home_redirect():
    path= reverse("home")
    request= RequestFactory().get(path)
    request.user = AnonymousUser()
    response = home(request)
    assert response.status_code == 302


@pytest.mark.django_db
def test_2_course_create():
    course = Course.objects.create(subject="AAS",catalog_number="3710", sub_and_cat="AAS 3710", class_section="001",class_number= 12798,class_title="African Worlds, Life Stories",instructor="Shutt,Lisa Toccafondi")
    assert course.subject == "AAS"
    assert course.catalog_number == "3710"
    assert course.class_section!= "002"

@pytest.mark.django_db
def test_3_classes_page():
    path = reverse("course_list")
    request= RequestFactory().get(path)
    request.user= AnonymousUser()
    response = course_list(request)
    assert response.status_code== 200

@pytest.mark.django_db
def test_4_student_home():
    path = reverse("student-home")
    request= RequestFactory().get(path)
    requestUser= User.objects.create_user(username='bbb', email="bob@gmail.com")
    testUser = AppUser.objects.create(email="bob@gmail.com", first_name="bob", last_name="tom", user_role= AppUser.STUDENT)
    request.user= requestUser
    response = student_home(request)
    assert response.status_code== 200

@pytest.mark.django_db
def test_5_tutor_home():
    path = reverse("tutor-home")
    request= RequestFactory().get(path)
    requestUser= User.objects.create_user(username='bbb', email="bob@gmail.com")
    testUser = AppUser.objects.create(email="bob@gmail.com", first_name="bob", last_name="tom", user_role= AppUser.TUTOR)
    request.user= requestUser
    response = tutor_home(request)
    assert response.status_code== 200

@pytest.mark.django_db
def test_6_student_home_redirect():
    path = reverse("student-home")
    request= RequestFactory().get(path)
    requestUser= User.objects.create_user(username='bbb', email="bob@gmail.com")
    testUser = AppUser.objects.create(email="bob@gmail.com", first_name="bob", last_name="tom", user_role= AppUser.TUTOR)
    request.user= requestUser
    response = student_home(request)
    assert response.status_code== 302

@pytest.mark.django_db
def test_7_tutor_home_redirect():
    path = reverse("tutor-home")
    request= RequestFactory().get(path)
    requestUser= User.objects.create_user(username='bbb', email="bob@gmail.com")
    testUser = AppUser.objects.create(email="bob@gmail.com", first_name="bob", last_name="tom", user_role= AppUser.STUDENT)
    request.user= requestUser
    response = tutor_home(request)
    assert response.status_code== 302

@pytest.mark.django_db
def test_8_post_session():
    path = reverse("post-session")
    request=RequestFactory().post(path)
    request.user = User.objects.create_user(username='b', email='test@test.com')
    form_mock = MagicMock()
    form_mock.is_valid.return_value = True
    with patch('myapp.views.SessionForm', return_value=form_mock):
        response = post_session(request)
    assert form_mock.is_valid.called
    assert response.status_code==302

@pytest.mark.django_db
def test_9_post_session_fail():
    path = reverse("post-session")
    request=RequestFactory().post(path)
    request.user = User.objects.create_user(username='b', email='test@test.com')
    form_mock = MagicMock()
    form_mock.is_valid.return_value = False
    with patch('myapp.views.SessionForm', return_value=form_mock):
        response = post_session(request)
    assert form_mock.is_valid.called
    assert response.status_code==200

@pytest.mark.django_db
def test_10_tutor_session_view():
    path = reverse("current-sessions")
    request = RequestFactory().get(path)
    requestUser = User.objects.create_user(username='bbb', email="bob@gmail.com")
    testUser = AppUser.objects.create(email="bob@gmail.com", first_name="bob", last_name="tom",user_role=AppUser.TUTOR)
    request.user = requestUser
    response = current_sessions(request)
    assert response.status_code==200

@pytest.mark.django_db
def test_11_student_session_view():
    path = reverse("current-appointments")
    request = RequestFactory().get(path)
    requestUser = User.objects.create_user(username='bbb', email="bob@gmail.com")
    testUser = AppUser.objects.create(email="bob@gmail.com", first_name="bob", last_name="tom",user_role=AppUser.STUDENT)
    request.user = requestUser
    response = current_appointments(request)
    assert response.status_code==200
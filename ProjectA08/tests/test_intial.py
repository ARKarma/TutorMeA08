import pytest
from django.urls import reverse
from myapp.views import home, course_list, student_home
from django.contrib.auth.models import AnonymousUser, User, AbstractBaseUser, UserManager
from django.test import RequestFactory
from myapp.models import Course, AppUser
from unittest.mock import Mock, MagicMock
import sqlite3

@pytest.mark.django_db
def test_home_redirect():
    path= reverse("home")
    request= RequestFactory().get(path)
    request.user = AnonymousUser()
    response = home(request)
    assert response.status_code == 302

@pytest.mark.django_db
def test_course_create():
    course = Course.objects.create(subject="AAS",catalog_number="3710", sub_and_cat="AAS 3710", class_section="001",class_number= 12798,class_title="African Worlds, Life Stories",instructor="Shutt,Lisa Toccafondi")
    assert course.subject == "AAS"
    assert course.catalog_number == "3710"
    assert course.class_section!= "002"

@pytest.mark.django_db
def test_classes_page():
    path = reverse("course_list")
    request= RequestFactory().get(path)
    request.user= AnonymousUser()
    response = course_list(request)
    assert response.status_code== 200

@pytest.mark.django_db
def test_student_home():
    path = reverse("student-home")
    request= RequestFactory().get(path)
    requestUser= User.objects.create_user(username='bbb', email="bob@gmail.com")
    testUser = AppUser.objects.create(email="bob@gmail.com", first_name="bob", last_name="tom", user_role= AppUser.STUDENT)
    request.user= requestUser
    response = student_home(request)
    assert response.status_code== 200

@pytest.mark.django_db
def test_tutor_home():
    path = reverse("tutor-home")
    request= RequestFactory().get(path)
    requestUser= User.objects.create_user(username='bbb', email="bob@gmail.com")
    testUser = AppUser.objects.create(email="bob@gmail.com", first_name="bob", last_name="tom", user_role= AppUser.TUTOR)
    request.user= requestUser
    response = student_home(request)
    assert response.status_code== 200

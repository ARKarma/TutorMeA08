import pytest
from django.urls import reverse
from myapp.views import home, course_list, student_home
from django.contrib.auth.models import AnonymousUser, User, AbstractBaseUser, UserManager
from django.test import RequestFactory
from myapp.models import Course, User
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




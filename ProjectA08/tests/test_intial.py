import pytest
from django.urls import reverse
from myapp.views import home
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from myapp.models import Course

@pytest.mark.django_db
def test_home_redirect():
    path= reverse("home")
    request= RequestFactory().get(path)
    request.user = AnonymousUser()
    response = home(request)
    print(response['location'])
    assert response.status_code == 302

# @pytest.mark.django_db
# def test_course_create():
#     course = Course.objects.create(subject="AAS",catalog_number="3710",class_section="001",class_number= 12798,class_title="African Worlds, Life Stories",class_topic_formal_desc="",instructor="Shutt,Lisa Toccafondi",enrollment_capacity=16,meeting_days="R",meeting_time_start="14:00:00", meeting_time_end="16:30:00",term="1228",term_desc="2022 Fall")
#     assert course.subject == "AAS"
#     assert course.catalog_number == "3710"
#     assert course.class_number!=12799

@pytest.mark.django_db
def test_course_in_database():
    course = Course.objects.filter(class_number="cs 3240")
    assert course.subject == "CS"
    assert course.catalog_number == "3240"


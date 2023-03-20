import pytest
from django.urls import reverse
from myapp.views import home
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory

@pytest.mark.django_db
def test_home():
    path= reverse("login")
    request= RequestFactory().get(path)
    request.user = AnonymousUser()
    response = home(request)
    assert response.status_code == 200

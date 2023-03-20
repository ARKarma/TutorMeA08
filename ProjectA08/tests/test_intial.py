from django.urls import reverse
from myapp.views import home

@pytest.mark.django_db
def test_home():
    path= reverse("")
    request= RequestFactory().get(path)
    response = home(request)
    assert response.status_code == 200

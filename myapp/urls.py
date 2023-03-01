from django.urls import path
from ProjectA08 import views

urlpatterns = [
    path('', views.index, name='index'),
]
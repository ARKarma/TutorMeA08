from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'template.html', {})
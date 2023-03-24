from django import forms
from .models import Session


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'description', 'price', 'date', 'start_time', 'end_time', 'max_students']
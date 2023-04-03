from django import forms
from .models import Session, Course


class SessionForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ['course', 'description', 'price', 'date', 'start_time', 'end_time', 'max_students', ]

    course = forms.ModelChoiceField(queryset=Course.objects.all())

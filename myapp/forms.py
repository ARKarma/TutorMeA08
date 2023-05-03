from django import forms
from .models import Session, Course, Booking


class SessionForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ['description', 'price', 'date',
                  'start_time', 'end_time', ]

    course = forms.ModelChoiceField(
        queryset=Course.objects.all()
    )


class BookingForm(forms.ModelForm):
    PAYMENT_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('venmo', 'Venmo'),
    )

    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES)

    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'contact', 'payment_method']

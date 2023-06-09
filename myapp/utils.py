from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Booking
from django.db.models import Q

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(session__date__day=day, booking_status='ACCEPTED').filter(Q(user=self.user) | Q(
            session__tutor=self.user))
        d = ''
        for event in events_per_day:
            d += f'<li> {event.session} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Booking.objects.filter(session__date__year=self.year, session__date__month=self.month,
                                        booking_status='ACCEPTED').filter(Q(user=self.user) |
                                                                          Q(session__tutor=self.user))

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
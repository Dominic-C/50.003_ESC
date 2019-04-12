from django import forms
from .models import Schedule
from login.models import User
import datetime as dt

usertypes = { 
    'professor': 1, 
    'sutdadmin': 2, 
    'coursecoordinators': 3, 
    'timetableplanner': 4, 
    'student' : 5
    } 

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
LOCATION_CHOICES = (
    # ('1', 'Think Tank 1'),
    # ('2', 'Think Tank 2'),
    # ('3', 'Think Tank 3'),
    # ('4', 'Cohort Classroom 1'),
    # ('5', 'Cohort Classroom 2'),
    # ('6', 'Cohort Classroom 3'),
    # ('7', 'Lecture Theatre 1'),
    # ('8', 'Lecture Theatre 2'),
    # ('9', 'Lecture Theatre 3'),
    ('1', 'any'),
    ('2', 'Lecture Theatre'),
)
class CreateSchedule(forms.ModelForm):
    # if location is LT, then check if time clashes in queryset
    queryset = Schedule.objects.all()

    lecturer = forms.ModelChoiceField(queryset=User.objects.filter(user_type=usertypes['professor'])) # TODO: change to Professor model in future
    
    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {'start_time': forms.Select(choices=HOUR_CHOICES),
        'end_time':forms.Select(choices=HOUR_CHOICES), 'location':forms.Select(choices=LOCATION_CHOICES)
        }

        # iff lecturer wants to book lt, then check if available.
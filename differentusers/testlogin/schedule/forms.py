from django import forms
from schedule.models import NewSchedule
from loginpage.models import User
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
    ('1', 'any'),
    ('2', 'Lecture Theatre'),
)
class CreateSchedule(forms.ModelForm):
    # if location is LT, then check if time clashes in queryset
    queryset = NewSchedule.objects.all()

    lecturer = forms.ModelChoiceField(queryset=User.objects.filter(user_type=usertypes['professor'])) # TODO: change to Professor model in future
    
    class Meta:
        model = NewSchedule
        fields = '__all__'
        widgets = {'start_time': forms.Select(choices=HOUR_CHOICES),
        'end_time':forms.Select(choices=HOUR_CHOICES), 'location':forms.Select(choices=LOCATION_CHOICES)
        }

        # iff lecturer wants to book lt, then check if available.
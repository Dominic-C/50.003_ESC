from django import forms
from schedule.models import Schedule
from loginpage.models import User
import datetime as dt
from django.contrib import messages

usertypes = {
    'professor': 1,
    'sutdadmin': 2,
    'coursecoordinators': 3,
    'timetableplanner': 4,
    'student': 5
}

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
LOCATION_CHOICES = (
    ('1', 'any'),
    ('2', 'Lecture Theatre'),
)


class CreateScheduleForm(forms.ModelForm):
    # if location is LT, then check if time clashes in queryset
    queryset = Schedule.objects.all()

    lecturer = forms.ModelChoiceField(queryset=User.objects.filter(
        user_type=usertypes['professor']))
    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {'location': forms.Select(choices=LOCATION_CHOICES),
                   'is_Finalized' : forms.HiddenInput(),
                   'is_Conflicting' : forms.HiddenInput(),
                   'is_Suggestion' : forms.HiddenInput(),
                   'initiated_By' : forms.HiddenInput(),
                   'day_Of_Week' : forms.HiddenInput()
                   }
        

    def save(self, conflict=0, commit=True):
        m = super(CreateScheduleForm, self).save(commit=False)
        # do custom stuff
        day = m.date.weekday() + 1
        m.day_Of_Week = day
        print("automatic day of week is: ", day)
        m.is_Suggestion = True
        if conflict == 1:
            m.is_Conflicting = True
        if commit:
            m.save()
        return m

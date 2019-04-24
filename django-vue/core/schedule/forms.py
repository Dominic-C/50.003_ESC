from django import forms
from .models import Schedule
from login.models import User
import datetime as dt

usertypes = {
    'professor': 1,
    'sutdadmin': 2,
    'coursecoordinators': 3,
    'timetableplanner': 4,
    'student': 5
}

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(7, 24)]
DURATION_CHOICES = [('{}'.format(x), '{:02d}'.format(x*15))
                    for x in range(1, 13)]
DAY_CHOICES = [('1', 'Monday'), ('2', 'Tuesday'),
               ('3', 'Wednesday'), ('4', 'Thursday'),
               ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')]

LOCATION_CHOICES = [('1', 'any'),
                    ('2', 'Lecture Theatre')]


# class CreateScheduleForm(forms.ModelForm):
#     # if location is LT, then check if time clashes in queryset
#     queryset = Schedule.objects.all()

#     lecturer = forms.ModelChoiceField(queryset=User.objects.filter(
#         user_type=usertypes['professor']))  # TODO: change to Professor model in future
#     initiated_By = forms.ModelChoiceField(queryset=User.objects.all())

#     class Meta:
#         model = Schedule
#         fields = '__all__'
#         exclude = ('initiated_By',)
#         widgets = {'start_Time': forms.Select(choices=HOUR_CHOICES),
#                    'event_Duration': forms.Select(choices=DURATION_CHOICES),
#                    'day_Of_Week': forms.Select(choices=DAY_CHOICES),
#                    'location': forms.Select(choices=LOCATION_CHOICES)
#                    }

#     def save(self, commit=True, conflict=0):
#         m = super(CreateScheduleForm, self).save(commit=False)
#         # do custom stuff
#         if conflict == 1:
#             m.is_Conflicting = True
#         if commit:
#             m.save()
#         return m

#         # iff lecturer wants to book lt, then check if available.


class CreateScheduleForm(forms.ModelForm):
    # if location is LT, then check if time clashes in queryset
    queryset = Schedule.objects.all()

    lecturer = forms.ModelChoiceField(queryset=User.objects.filter(
        user_type=usertypes['professor']))

    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {'location': forms.Select(choices=LOCATION_CHOICES),
                   'start_Time': forms.Select(choices=HOUR_CHOICES),
                   'event_Duration': forms.Select(choices=DURATION_CHOICES),
                   'is_Finalized': forms.HiddenInput(),
                   'is_Conflicting': forms.HiddenInput(),
                   'is_Suggestion': forms.HiddenInput(),
                   'initiated_By': forms.HiddenInput(),
                   'day_Of_Week': forms.HiddenInput(),
                   'is_classconflict': forms.HiddenInput(),
                   'is_profconflict': forms.HiddenInput()
                   }

    def save(self, location_conflict=0, class_conflict=0, prof_conflict=0, commit=True):
        m = super(CreateScheduleForm, self).save(commit=False)
        # do custom stuff
        day = m.date.weekday() + 1
        m.day_Of_Week = day
        print("automatic day of week is: ", day)
        m.is_Suggestion = True
        if location_conflict == 1:
            m.is_Conflicting = True
        if prof_conflict == 1:
            m.is_profconflict = True
        if class_conflict == 1:
            m.is_classconflict = True
        if commit:
            m.save()
        return m

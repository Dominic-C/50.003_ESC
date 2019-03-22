from django import forms
from schedule.models import Schedule
from loginpage.models import User


# form class not used
class CreateSchedule(forms.ModelForm):

    lecturer = forms.ModelChoiceField(queryset=User.objects.all()) # TODO: change to Professor model in future
    
    class Meta:
        model = Schedule
        fields = ['title','description','start_time','end_time', 'lecturer', 'location']
from django import forms
from schedule.models import Schedule

class CreateSchedule(forms.ModelForm):
    
    class Meta:
        model = Schedule
        fields = ['title','description','start_time','end_time', 'lecturer', 'location']
from django import forms
from schedule.models import Schedule

# form class not used
class CreateSchedule(forms.ModelForm):
    
    class Meta:
        model = Schedule
        fields = ['title','description','start_time','end_time', 'lecturer', 'location']
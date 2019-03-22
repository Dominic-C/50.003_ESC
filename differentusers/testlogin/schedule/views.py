from django.shortcuts import render
from django.views.generic import CreateView
from .models import Schedule
from .forms import CreateSchedule

# Create your views here.
class ScheduleListView(CreateView):
    model = Schedule
    template_name = "schedule/schedule_list.html"
    fields = ['title','description','start_time','end_time', 'lecturer', 'location']

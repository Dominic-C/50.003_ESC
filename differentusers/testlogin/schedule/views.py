from django.shortcuts import render
from django.views.generic import DetailView
from .models import Schedule

# Create your views here.
class ScheduleListView(DetailView):
    template_name = "schedule/schedule_list.html"
    queryset = Schedule.objects.all()
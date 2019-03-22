from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Schedule
from .forms import CreateSchedule
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
class ScheduleCreateView(CreateView):
    model = Schedule
    template_name = "schedule/schedule_create.html"
    fields = ['title','description','start_time','end_time', 'lecturer', 'location']

    def form_valid(self, form):
        form.save()
        return redirect('schedule:list')

class ScheduleListView(ListView):
	model = Schedule
	template_name = "schedule/schedule_list.html"
	queryset = Schedule.objects.all()
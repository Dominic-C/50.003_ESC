from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Schedule
from .forms import CreateSchedule
from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
class ScheduleCreateView(CreateView):
    model = Schedule
    template_name = "schedule/schedule_create.html"
    fields = '__all__'

    def form_valid(self, form):
        form.save()
        return redirect('schedule:list')

class ScheduleListView(ListView):
	model = Schedule
	template_name = "schedule/schedule_list.html"
	queryset = Schedule.objects.all()

def add_schedule(request):
    if request.method == "POST":
        form = CreateSchedule(request.POST) # creates form instance and binds form data to it. request.post contains form data
        # check if form is valid
        if form.is_valid():
            schedule_item = form.save(commit=False)
            schedule_item.save()
    else: # no post data, resulting in empty form.
        form = CreateSchedule()
    return render(request, 'schedule/createSchedule_form.html', {'form': form})

def serialized_schedule(request):
    queryset = Schedule.objects.all()
    queryset = serializers.serialize('json', queryset)
    return HttpResponse(queryset, content_type="application/json")
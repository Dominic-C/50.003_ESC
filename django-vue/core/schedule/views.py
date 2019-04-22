from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Schedule
from .forms import CreateScheduleForm
from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers
from django.http import HttpResponse, Http404
from login.decorators import professor_required, drafting_required, beforefirstdraft_required
from django.contrib.auth.decorators import login_required

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
    ser_data = serializers.serialize("json", queryset)

    def get_context_data(self, **kwargs):
        context = super(ScheduleListView, self).get_context_data(**kwargs)
        queryset = Schedule.objects.all()
        context['jsonset'] = serializers.serialize("json", queryset)
        return context


@professor_required
@login_required
@drafting_required
def add_schedule(request):
    if request.method == "POST":
        # creates form instance and binds form data to it. request.post contains form data
        form = CreateScheduleForm(request.POST)
        # check if form is valid
        if form.is_valid():
            print(Schedule.objects.filter(location=2))
            print(form.cleaned_data['start_Time'])
            if(Schedule.objects.filter(location=2)):
                lectureTheaterBookings = Schedule.objects.filter(location=2)
                conflict = False

                for i in lectureTheaterBookings:
                    if (form.cleaned_data['start_Time'] >= i.start_Time or form.cleaned_data['end_time'] <= i.end_time) and form.cleaned_data['date'] == i.date:
                        conflict = True
                        schedule_item = form.save(commit=False, conflict=1)
                        schedule_item.save()
                        raise Http404('time conflict')

            schedule_item = form.save(commit=False)
            schedule_item.save()
    else:  # no post data, resulting in empty form.
        form = CreateScheduleForm()

    queryset = Schedule.objects.all()
    jsonset = serializers.serialize('json', queryset)
    context = {
        'form': form,
        'jsonset': queryset
    }
    return render(request, 'schedule/createSchedule_form.html', context)

# def serialized_schedule(request):
#     queryset = Schedule.objects.all()
#     queryset = serializers.serialize('json', queryset)
#     return HttpResponse(queryset, content_type="application/json")

from django.shortcuts import render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView, View)
from .models import Schedule
from .forms import CreateScheduleForm
from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers
from django.http import HttpResponse, Http404, HttpResponseRedirect 
from loginpage.decorators import professor_required, drafting_required, beforefirstdraft_required
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import datetime as dt
from django.contrib import messages
# Create your views here.


# class ScheduleCreateView(CreateView):
#     model = Schedule
#     template_name = "schedule/schedule_create.html"
#     fields = '__all__'

#     def form_valid(self, form):
#         form.save()
#         return redirect('schedule:list')


# class ScheduleListView(ListView):
#     model = NewSchedule
#     template_name = "schedule/schedule_list.html"
#     queryset = NewSchedule.objects.all()
#     ser_data = serializers.serialize("json", queryset)

#     def get_context_data(self, **kwargs):
#         context = super(ScheduleListView, self).get_context_data(**kwargs)
#         context['jsonset'] = self.ser_data
#         context['component'] = "calendar.js"
#         return context

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
            print((dt.datetime.combine(dt.date(1,1,1),form.cleaned_data['start_Time']) + timedelta( minutes = form.cleaned_data['event_Duration'] * 15 )).time())
            if(Schedule.objects.filter(location=2)):
                lectureTheaterBookings = Schedule.objects.filter(location=2)
                conflict = False
                
                for i in lectureTheaterBookings:
                    i_start_time = i.start_Time
                    i_end_time = (dt.datetime.combine(dt.date(1,1,1),i_start_time) + timedelta(minutes = i.event_Duration * 15)).time()
                    print("event ", i, i_start_time, i_end_time)
                    if (form.cleaned_data['start_Time'] >= i_start_time and form.cleaned_data['start_Time'] <= i_end_time) and form.cleaned_data['date'] == i.date:
                        conflict = True
                        schedule_item = form.save(commit=False, conflict=1)
                        schedule_item.save()
                        messages.warning(request, 'Your suggestion clashes with another existing schedule.')
                        return redirect('schedule:addschedule')

            messages.success(request, 'Your suggestion was saved successfully.')
            schedule_item = form.save(commit=False)
            schedule_item.save()
    else:  # no post data, resulting in empty form.
        form = CreateScheduleForm()
    
    context = {
        'form': form,
    }
    return render(request, 'schedule/createSchedule_form.html', context)


@professor_required
@login_required
@drafting_required
def deconflict_suggestions(request):
    # if request.method == "POST":

    return None

@professor_required
@login_required
@drafting_required
def finalize_suggestion(request):
    # if request.method == "POST":

    return None



# def serialized_schedule(request):
#     queryset = Schedule.objects.all()
#     queryset = serializers.serialize('json', queryset)
#     return HttpResponse(queryset, content_type="application/json")
class ModifyScheduleListView(ListView):
    template_name = 'modifyschedule/modifyschedulelist.html'
    all_obj = Schedule.objects.all()
    for i in all_obj:
        print(i.pk)

    def get_queryset(self):
        return Schedule.objects.filter(is_Event=False)

class ModifyScheduleEditView(UpdateView):
    model = Schedule
    template_name = 'modifyschedule/modifyscheduleeditview.html'
    # form_class = SubmitCourseDetails
    fields = '__all__'

    # def form_valid(self, form):
    #     details = form.save(commit=False)
    #     details.first_name = self.request.user.first_name
    #     details.last_name = self.request.user.last_name
    #     details.user_type = self.request.user.user_type
    #     details.created_by = self.request.user
    #     details.save()
    #     return redirect('schedule:allschedules')

    def get_queryset(self):
        # only allow current User to edit the details he has submitted
        return Schedule.objects.all()


# class DetailsDeleteView(DeleteView):
#     model = Schedule
#     template_name = 'coursedetails/preferences_confirm_delete.html'

#     def get_success_url(self):
#         return reverse('professors:details')

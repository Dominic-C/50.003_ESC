from django.shortcuts import render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView, View)
from .models import Schedule
from .forms import CreateScheduleForm
from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers
from django.http import HttpResponse, Http404
from login.decorators import professor_required, drafting_required, beforefirstdraft_required
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from datetime import timedelta
import datetime as dt
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator

# from django.ical.views import ICalFeed

# Create your views here.


# class ScheduleFeed(ICalFeed):
#     """
#     Calendar output
#     """
#     product_id = "-//sutdcal.com//"
#     timezone = "UTC+8"
#     file_name = "calendar.ics"

#     def items(self):
#         return Schedule.objects.all().order_by('-start_datetime')

#     def item_title(self, item):
#         return item.

def save_ical(request):
    template_name = "schedule/schedule_list.html"
    records = Schedule.objects.all()
    entries = []
    count = 0
    decompressed = model_to_dict(
        Schedule, fields=[field.name for field in Schedule._meta.fields])
    for row in decompressed:
        entry = decompressed[row]
        entries.append(entry)
    return render(request, template_name)


@professor_required
@login_required
@drafting_required
def add_schedule(request):
    if request.method == "POST":
        # creates form instance and binds form data to it. request.post contains form data
        form = CreateScheduleForm(request.POST)
        # check if form is valid
        if form.is_valid():
            # print(Schedule.objects.filter(location=2))
            # print((dt.datetime.combine(dt.date(1,1,1),form.cleaned_data['start_Time']) + timedelta( minutes = form.cleaned_data['event_Duration'] * 15 )).time())
            lectureTheaterBookings = Schedule.objects.filter(location=2)
            if(form.cleaned_data['location'] == 2):  # If Lecture Theatre

                for i in lectureTheaterBookings:
                    i_start_time = i.start_Time
                    i_end_time = (dt.datetime.combine(dt.date(
                        1, 1, 1), i_start_time) + timedelta(minutes=i.event_Duration * 15)).time()
                    print("event ", i, i_start_time, i_end_time)
                    # If start time is inside
                    if (form.cleaned_data['start_Time'] >= i_start_time and form.cleaned_data['start_Time'] <= i_end_time) and form.cleaned_data['date'] == i.date:

                        schedule_item = form.save(
                            commit=False, location_conflict=1)
                        schedule_item.save()
                        # break
                        messages.warning(
                            request, 'Your suggestion requires a Lecture Theatre that is not available at this time.')
                        break
                        # return redirect('schedule:addschedule')

            lecturer = str(form.cleaned_data['lecturer'])
            for i in Schedule.objects.all():  # check against all schedule objects
                i_start_time = i.start_Time
                i_end_time = (dt.datetime.combine(dt.date(
                    1, 1, 1), i_start_time) + timedelta(minutes=i.event_Duration * 15)).time()

                # If start time is inside
                if (form.cleaned_data['start_Time'] >= i_start_time and form.cleaned_data['start_Time'] <= i_end_time) and form.cleaned_data['date'] == i.date and lecturer == i.lecturer:
                    schedule_item = form.save(
                        commit=False, prof_conflict=1)
                    schedule_item.save()
                    # break
                    messages.warning(
                        request, 'Your suggestion causes this professor to have two classes at the same time.')
                    break
                    # return redirect('schedule:addschedule')

            class_enrolled = str(form.cleaned_data['class_Enrolled'])
            for i in Schedule.objects.all():  # check against all schedule objects
                i_start_time = i.start_Time
                i_end_time = (dt.datetime.combine(dt.date(
                    1, 1, 1), i_start_time) + timedelta(minutes=i.event_Duration * 15)).time()

                # If start time is inside
                if (form.cleaned_data['start_Time'] >= i_start_time and form.cleaned_data['start_Time'] <= i_end_time) and form.cleaned_data['date'] == i.date and class_enrolled == i.class_Enrolled:
                    schedule_item = form.save(
                        commit=False, class_conflict=1)
                    schedule_item.save()
                    # break
                    messages.warning(
                        request, 'Your suggestion clashes with another class for this cohort.')
                    break
                    # return redirect('schedule:addschedule')

            messages.success(
                request, 'Your suggestion was saved successfully.')
            schedule_item = form.save(commit=False)
            schedule_item.save()
    else:  # no post data, resulting in empty form.
        form = CreateScheduleForm()

    context = {
        'form': form,
    }
    return render(request, 'schedule/createSchedule_form.html', context)

    # def serialized_schedule(request):
    #     queryset = Schedule.objects.all()
    #     queryset = serializers.serialize('json', queryset)
    #     return HttpResponse(queryset, content_type="application/json")


# @method_decorator([login_required], name='dispatch')
class ScheduleCreateView(CreateView):
    model = Schedule
    template_name = "schedule/schedule_create.html"
    fields = '__all__'

    def form_valid(self, form):
        details = form.save(commit=False)
        details.initiated_By = self.request.user
        details.save()
        return redirect('schedule:list')


@method_decorator([login_required], name='dispatch')
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

    def form_valid(self, form):
        modify = form.save(commit=False)
        print(type(self))
        modify.course_Name = form.cleaned_data['course_Name']
        modify.pillar_Type = form.cleaned_data['pillar_Type']
        modify.event_Name = form.cleaned_data['event_Name']
        modify.description = form.cleaned_data['description']
        modify.date = form.cleaned_data['date']
        modify.start_Time = form.cleaned_data['start_Time']
        modify.event_Duration = form.cleaned_data['event_Duration']
        modify.lecturer = form.cleaned_data['lecturer']
        modify.class_Enrolled = form.cleaned_data['class_Enrolled']
        modify.location = form.cleaned_data['location']
        modify.is_Event = form.cleaned_data['is_Event']
        modify.initiated_By = form.cleaned_data['initiated_By']
        modify.is_Conflicting = form.cleaned_data['is_Conflicting']
        modify.day_Of_Week = form.cleaned_data['day_Of_Week']
        modify.is_Suggestion = False
        modify.is_Finalized = True
        modify.save()
        return redirect('schedule:allschedules')

    def get_queryset(self):
        # only allow current User to edit the details he has submitted
        return Schedule.objects.all()


class ModifyScheduleDeleteView(DeleteView):
    model = Schedule
    template_name = 'modifyschedule/modifyschedule_delete.html'

    def get_success_url(self):
        return reverse('schedule:allschedules')


@method_decorator([login_required], name='dispatch')
class ViewDraftCalendar(ListView):
    model = Schedule
    template_name = 'schedule/draftcalendar.html'

    def get_context_data(self, **kwargs):
        context = super(ViewDraftCalendar, self).get_context_data(**kwargs)
        objects = Schedule.objects.all()
        phase = self.request.user.phase
        context['jsonset'] = serializers.serialize("json", objects)
        context['phase'] = serializers.serialize("json", phase)
        # context['userdata'] = serializers.serialize("json", user)
        # context['jsonphase'] = serializers.serialize("json", phase)
        return context

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)

from ..decorators import coordinator_required
from ..forms import CoordinatorSignUpForm
from ..models import User
from schedule.models import Schedule
from datetime import timedelta
import datetime as dt


usertypes = {
    'professor': 1,
    'sutdadmin': 2,
    'coursecoordinators': 3,
    'timetableplanner': 4,
    'student': 5
}


class CoordinatorSignUpView(CreateView):
    model = User
    form_class = CoordinatorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'coordinator'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        userdetail = form.save(commit=False)
        try:
            userdetail.phase = User.objects.filter(
                user_type=usertypes['professor'])[0].phase
        except:
            userdetail.phase = 1
        userdetail = form.save()
        login(self.request, userdetail)
        return redirect('coordinators:coordinator_main')


@method_decorator([login_required, coordinator_required], name='dispatch')
class CoordinatorMainView(TemplateView):
    template_name = 'classroom/coordinators/coordinator_main.html'


@method_decorator([login_required, coordinator_required], name='dispatch')
class CoordinatorAccountsListView(ListView):
    template_name = 'classroom/coordinators/accountslist.html'
    queryset = User.objects.all()


@method_decorator([login_required, coordinator_required], name='dispatch')
class ScheduleEditView(UpdateView):
    model = Schedule
    template_name = "schedule/editsuggest.html"
    fields = ['lecturer', 'class_Enrolled', 'date',
              'start_Time', 'event_Duration', 'location']

    def form_valid(self, form):
        # PILLAR_STRTOINT = {
        #     'ASD': 0, 'ISTD': 1, 'EPD': 2, 'ESD': 3, 'FRESHMORE': 4, 'MASTERS': 5, 'PHD': 6, 'NONE': 7}

        details = form.save(commit=False)
        details.course_Name = self.object.course_Name
        details.pillar_Type = self.object.pillar_Type
        details.event_Name = self.object.event_Name
        details.description = self.object.description
        details.is_Event = self.object.is_Event
        details.initiated_By = self.object.initiated_By
        details.day_Of_Week = self.object.day_Of_Week
        details.is_classconflict = self.object.is_classconflict
        details.is_profconflict = self.object.is_profconflict
        details.is_Suggestion = self.object.is_Suggestion
        details.is_Finalized = self.object.is_Finalized
        details.is_Approved = self.object.is_Approved

        # Check class enrolled
        class_enrolled = str(form.cleaned_data['class_Enrolled'])
        for i in Schedule.objects.all():  # check against all schedule objects
            i_start_time = i.start_Time
            i_end_time = (dt.datetime.combine(dt.date(
                1, 1, 1), i_start_time) + timedelta(minutes=i.event_Duration * 15)).time()
            # If start time is inside
            if (form.cleaned_data['start_Time'] >= i_start_time and form.cleaned_data['start_Time'] <= i_end_time) and form.cleaned_data['date'] == i.date and class_enrolled == i.class_Enrolled:
                details.is_classconflict = True
                break

        # check LT
        lectureTheaterBookings = Schedule.objects.filter(location=2)
        if(form.cleaned_data['location'] == 2):  # If Lecture Theatre
            for i in lectureTheaterBookings:
                i_start_time = i.start_Time
                i_end_time = (dt.datetime.combine(dt.date(
                    1, 1, 1), i_start_time) + timedelta(minutes=i.event_Duration * 15)).time()
                print("event ", i, i_start_time, i_end_time)
                # If start time is inside
                if (form.cleaned_data['start_Time'] >= i_start_time and form.cleaned_data['start_Time'] <= i_end_time) and form.cleaned_data['date'] == i.date:
                    details.is_Conflicting = True

        # Check cohort
        class_enrolled = str(form.cleaned_data['class_Enrolled'])
        for i in Schedule.objects.all():  # check against all schedule objects
            i_start_time = i.start_Time
            i_end_time = (dt.datetime.combine(dt.date(
                1, 1, 1), i_start_time) + timedelta(minutes=i.event_Duration * 15)).time()

            # If start time is inside
            if (form.cleaned_data['start_Time'] >= i_start_time and form.cleaned_data['start_Time'] <= i_end_time) and form.cleaned_data['date'] == i.date and class_enrolled == i.class_Enrolled:
                details.is_classconflict = True

        details.save()
        return redirect('coordinators:conflicts')

    def get_queryset(self):
        return Schedule.objects.all()


@method_decorator([login_required, coordinator_required], name='dispatch')
class ScheduleConflictView(ListView):
    model = Schedule
    template_name = "schedule/conflictview.html"

    def get_queryset(self):
        q1 = Schedule.objects.filter(is_Conflicting=True)
        q2 = Schedule.objects.filter(is_profconflict=True)
        q3 = Schedule.objects.filter(is_classconflict=True)
        q12 = q1.union(q2)
        return q12.union(q3)

    def get_context_data(self, **kwargs):
        context = super(ScheduleConflictView, self).get_context_data(**kwargs)
        q1 = Schedule.objects.filter(is_Conflicting=True)
        q2 = Schedule.objects.filter(is_profconflict=True)
        q3 = Schedule.objects.filter(is_classconflict=True)
        q12 = q1.union(q2)
        context['conflicts'] = serializers.serialize("json", q12.union(q3))
        return context


@method_decorator([login_required, coordinator_required], name='dispatch')
class ScheduleApproveView(UpdateView):
    model = Schedule
    template_name = 'schedule/approve.html'
    fields = ['is_Approved']

    def form_valid(self, form):
        details = form.save(commit=False)
        details.is_Approved = True
        details.course_Name = self.object.course_Name
        details.pillar_Type = self.object.pillar_Type
        details.event_Name = self.object.event_Name

        details.lecturer = self.object.lecturer
        details.class_Enrolled = self.object.class_Enrolled
        details.date = self.object.date
        details.start_Time = self.object.start_Time
        details.event_Duration = self.object.event_Duration

        details.description = self.object.description
        details.is_Event = self.object.is_Event
        details.initiated_By = self.object.initiated_By
        details.day_Of_Week = self.object.day_Of_Week
        details.is_classconflict = self.object.is_classconflict
        details.is_profconflict = self.object.is_profconflict
        details.is_Suggestion = self.object.is_Suggestion
        details.is_Finalized = self.object.is_Finalized

        return redirect('coordinators:conflicts')

    def get_success_url(self):
        return redirect('coordinators:conflicts')

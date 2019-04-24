from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView

import datetime

from ..decorators import sutdadmin_required
from ..forms import SutdAdminSignUpForm
from ..models import User
from schedule.models import Schedule

usertypes = { 
    'professor': 1, 
    'sutdadmin': 2, 
    'coursecoordinators': 3, 
    'timetableplanner': 4, 
    'student' : 5
    }


class SutdAdminSignUpView(CreateView):
    model = User
    form_class = SutdAdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'sutdadmin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        userdetail = form.save(commit=False)
        try:
            userdetail.phase = User.objects.filter(user_type=usertypes['professor'])[0].phase
        except:
            userdetail.phase = 1
        userdetail = form.save()
        login(self.request, userdetail)
        return redirect('sutdadmin:sutdadmin_main')


@method_decorator([login_required, sutdadmin_required], name='dispatch')
class SutdAdminMainView(TemplateView):
    template_name = 'classroom/sutdadmin/sutdadmin_main.html'


@method_decorator([login_required, sutdadmin_required], name='dispatch')
class MakeBookingView(CreateView):
    model = Schedule
    template_name = 'classroom/sutdadmin/makebooking.html'
    fields = ['event_Name', 'lecturer', 'description', 'date', 'start_Time', 'event_Duration', 'location']

    def form_valid(self, form):
        details = form.save(commit=False)
        details.course_Name = ""
        details.pillar_Type = 7
        details.class_Enrolled = ""
        details.is_Event = True
        details.initiated_By = "Nobody"
        details.is_Conflicting = False
        day = form.cleaned_data['date'].weekday() + 1      # cause weekday() returns from 0 to 6, not 1 to 7
        details.day_Of_Week = day
        details.save()
        return redirect('sutdadmin:bookings')

@method_decorator([login_required, sutdadmin_required], name='dispatch')
class BookingList(ListView):
    template_name = 'classroom/sutdadmin/bookinglist.html'

    def get_queryset(self):
        # returns Events submited by the current User
        return Schedule.objects.filter(is_Event=True).order_by('date')

@method_decorator([login_required, sutdadmin_required], name='dispatch')
class EditBookingView(UpdateView):
    model = Schedule
    template_name = 'classroom/sutdadmin/editbooking.html'
    fields = ['event_Name', 'lecturer', 'description', 'date', 'start_Time', 'event_Duration', 'location']

    def form_valid(self, form):
        details = form.save(commit=False)
        details.course_Name = ""
        details.pillar_Type = 7
        details.class_Enrolled = ""
        details.is_Event = True
        details.initiated_By = "Nobody"
        details.is_Conflicting = False
        day = form.cleaned_data['date'].weekday() + 1      # cause weekday() returns from 0 to 6, not 1 to 7
        details.day_Of_Week = day
        details.save()
        return redirect('sutdadmin:bookings')

    def get_queryset(self):
        # only allow current User to edit events
        return Schedule.objects.filter(is_Event=True)


@method_decorator([login_required, sutdadmin_required], name='dispatch')
class DeleteBookingView(DeleteView):
    model = Schedule
    template_name = 'classroom/sutdadmin/event_confirm_delete.html'

    def get_success_url(self):
        return reverse('sutdadmin:bookings')



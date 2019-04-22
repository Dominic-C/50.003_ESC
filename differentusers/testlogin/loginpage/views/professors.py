from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView, View)
from django.core import serializers

from ..decorators import professor_required, drafting_required, beforefirstdraft_required
from ..forms import ProfessorSignUpForm, SubmitCourseDetails
from ..models import User, Preferences


usertypes = {
    'professor': 1,
    'sutdadmin': 2,
    'coursecoordinators': 3,
    'timetableplanner': 4,
    'student': 5
}


class ProfessorSignUpView(CreateView):
    model = User
    form_class = ProfessorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'professor'
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
        return redirect('professors:professor_main')


@method_decorator([login_required, professor_required], name='dispatch')
class ProfessorMainView(TemplateView):
    template_name = 'classroom/professors/professor_main.html'


@method_decorator([login_required, professor_required, beforefirstdraft_required], name='dispatch')
class SubmitCourseDetailsView(CreateView):
    model = Preferences
    fields = ['subject_code', 'subject_name', 'cohort_size', 'cohort_num']
    template_name = 'coursedetails/submitdetails.html'

    def form_valid(self, form):
        details = form.save(commit=False)
        details.first_name = self.request.user.first_name
        details.last_name = self.request.user.last_name
        details.user_type = self.request.user.user_type
        details.created_by = self.request.user
        details.save()
        return redirect('professors:details')


@method_decorator([login_required, professor_required, beforefirstdraft_required], name='dispatch')
class DetailsListView(ListView):
    template_name = 'coursedetails/detailslist.html'
    # queryset = Preferences.objects.all()

    def get_queryset(self):
        # returns Preferences submited by the current User
        return Preferences.objects.filter(created_by=self.request.user)


@method_decorator([login_required, professor_required, beforefirstdraft_required], name='dispatch')
class DetailsEditView(UpdateView):
    model = Preferences
    template_name = 'coursedetails/editdetails.html'
    # form_class = SubmitCourseDetails
    fields = ['subject_code', 'subject_name', 'cohort_size', 'cohort_num']

    def form_valid(self, form):
        details = form.save(commit=False)
        details.first_name = self.request.user.first_name
        details.last_name = self.request.user.last_name
        details.user_type = self.request.user.user_type
        details.created_by = self.request.user
        details.save()
        return redirect('professors:details')

    def get_queryset(self):
        # only allow current User to edit the details he has submitted
        return Preferences.objects.filter(created_by=self.request.user)


@method_decorator([login_required, professor_required, beforefirstdraft_required], name='dispatch')
class DetailsDeleteView(DeleteView):
    model = Preferences
    template_name = 'coursedetails/preferences_confirm_delete.html'

    def get_success_url(self):
        return reverse('professors:details')



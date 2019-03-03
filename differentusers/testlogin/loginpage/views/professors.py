from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView, FormView)

from ..decorators import professor_required
from ..forms import ProfessorSignUpForm, SubmitCourseDetails
from ..models import User, Preferences


class ProfessorSignUpView(CreateView):
    model = User
    form_class = ProfessorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'professor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('professors:professor_main')


@method_decorator([login_required, professor_required], name='dispatch')
class ProfessorMainView(TemplateView):
    template_name = 'classroom/professors/professor_main.html'



@method_decorator([login_required, professor_required], name='dispatch')
class SubmitCourseDetailsView(CreateView):
    model = Preferences
    fields = ['subject_code', 'subject_name', 'cohort_size', 'cohort_num']
    template_name = 'coursedetails/submitdetails.html'

    def form_valid(self, form):
        details = form.save(commit=False)
        details.first_name = self.request.user.first_name
        details.last_name = self.request.user.last_name
        details.user_type = self.request.user.user_type
        details.save()
        return redirect('professors:details')
    

@method_decorator([login_required, professor_required], name='dispatch')
class DetailsView(ListView):
    template_name = 'coursedetails/detailslist.html'
    queryset = Preferences.objects.all()


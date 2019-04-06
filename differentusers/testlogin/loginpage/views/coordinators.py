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
                                  UpdateView, TemplateView)

from ..decorators import coordinator_required
from ..forms import CoordinatorSignUpForm
from ..models import User

usertypes = { 
    'professor': 1, 
    'sutdadmin': 2, 
    'coursecoordinators': 3, 
    'timetableplanner': 4, 
    'student' : 5
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
            userdetail.phase = User.objects.filter(user_type=usertypes['professor'])[0].phase
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


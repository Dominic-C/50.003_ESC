from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView

from ..decorators import sutdadmin_required
from ..forms import SutdAdminSignUpForm
from ..models import User

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


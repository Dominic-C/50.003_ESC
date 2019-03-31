import csv

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView, View)
from django.http import HttpResponse
from django.template import Context, loader

from ..serializers import PreferencesSerializer
from ..decorators import planner_required
from ..forms import PlannerSignUpForm
from ..models import User, Preferences


class PlannerSignUpView(CreateView):
    model = User
    form_class = PlannerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'planner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('planners:planner_main')


@method_decorator([login_required, planner_required], name='dispatch')
class PlannerMainView(TemplateView):
    template_name = 'classroom/planners/planner_main.html'


class PreferencesCSVExportView(View):
    serializer_class = PreferencesSerializer

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        
        serializer = self.get_serializer(
            Preferences.objects.all(),
            many=True
        )
        header = PreferencesSerializer.Meta.fields
        
        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        
        return response
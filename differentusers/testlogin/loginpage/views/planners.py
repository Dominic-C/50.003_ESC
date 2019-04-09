import csv, io

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView, View)
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader

from ..serializers import PreferencesSerializer
from ..decorators import planner_required
from ..forms import PlannerSignUpForm
from ..models import User, Preferences, Lesson

usertypes = { 
    'professor': 1, 
    'sutdadmin': 2, 
    'coursecoordinators': 3, 
    'timetableplanner': 4, 
    'student' : 5
    }


class PlannerSignUpView(CreateView):
    model = User
    form_class = PlannerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'planner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        userdetail = form.save(commit=False)
        try:
            userdetail.phase = User.objects.filter(user_type=usertypes['professor'])[0].phase
        except:
            userdetail.phase = 1
        userdetail = form.save()
        login(self.request, userdetail)
        return redirect('planners:planner_main')


@method_decorator([login_required, planner_required], name='dispatch')
class PlannerMainView(TemplateView):
    template_name = 'classroom/planners/planner_main.html'

@method_decorator([login_required, planner_required], name='dispatch')
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

        # csv.DictWriter requires the input to .writerow to be a dictionary
        fieldnames = ['First Name', 'Last Name', 'Subject Code', 'Subject Name', 'Cohort Size', 'Number of Cohorts']
        # create a dictionary with header as keys and modified headernames as the values
        writer.writerow(dict(zip(header, fieldnames)))
        # writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        
        return response


@method_decorator([login_required, planner_required], name='dispatch')
class CurrentPhase(TemplateView):
    template_name = 'classroom/planners/planner_currentphase.html'


@method_decorator([login_required, planner_required], name='dispatch')
class NextPhase(View):

    def get(self, request, *args, **kwargs):
        current_phase = self.request.user.phase
        # change phase to next phase
        if (current_phase < 3):
            User.objects.all().update(phase=current_phase+1)
        # to reset
        # User.objects.all().update(phase=1)
        return redirect('planners:currentphase')

@method_decorator([login_required, planner_required], name='dispatch')
class PreviousPhase(View):

    def get(self, request, *args, **kwargs):
        current_phase = self.request.user.phase
        # change phase to previous phase
        if (current_phase > 1 ):
            User.objects.all().update(phase=current_phase-1)
        # to reset
        # User.objects.all().update(phase=1)
        return redirect('planners:currentphase')


@login_required
@planner_required
def csv_upload(request):
    template = "classroom/planners/phaser_upload.html"

    prompt = {
        'order': "Order of the CSV should be Pillar, Course Name, Title, Location, Class Enrolled, Day of Week, Duration"
    }

    if request.method == "GET":
        return render(request, template, prompt)

    try:
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "This file is not a .csv file")

        #if file is too large
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))

        data_set = csv_file.read().decode('utf-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Lesson.objects.update_or_create(
                pillar=column[0],
                course_name=column[1],
                title=column[2],
                location=column[3],
                class_enrolled=column[4],
                day_of_week=column[5],
                duration=column[6],)

        context = {}
        messages.success(request, 'File upload successful')
        return render(request, template, context)

    except Exception as e:
        messages.error(request,"Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file! Check your format and for empty rows!")
        return HttpResponseRedirect(reverse("planners:uploaddata"))


    # csv_file = request.FILES['file']

    # if not csv_file.name.endswith('.csv'):
    #     messages.error(request, "This file is not a .csv file")

    # data_set = csv_file.read().decode('utf-8')
    # io_string = io.StringIO(data_set)
    # next(io_string)
    # for column in csv.reader(io_string, delimiter=',', quotechar="|"):
    #     _, created = Example.objects.update_or_create(
    #         class_number=column[0],
    #         day=column[1],
    #     )

    # context = {}
    # messages.success(request, 'File upload successful')
    # return render(request, template, context)



import csv
import io

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
from ..decorators import planner_required, finalisation_required, drafting_required
from ..forms import PlannerSignUpForm
from ..models import User, Preferences, Lesson
from schedule.models import Schedule

usertypes = {
    'professor': 1,
    'sutdadmin': 2,
    'coursecoordinators': 3,
    'timetableplanner': 4,
    'student': 5
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
            userdetail.phase = User.objects.filter(
                user_type=usertypes['professor'])[0].phase
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
        fieldnames = ['First Name', 'Last Name', 'Subject Code',
                      'Subject Name', 'Cohort Size', 'Number of Cohorts']
        # create a dictionary with header as keys and modified headernames as the values
        writer.writerow(dict(zip(header, fieldnames)))
        # writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


@method_decorator([login_required, planner_required], name='dispatch')
class SampleDownloadView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sample.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['Course Name', "Pillar", "Event Name", "Description", "Date", "Start Time",
                         "Event Duration", "Lecturer", "Class Enrolled", "Location", "Initiated By", 'Day of Week'])
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
        if (current_phase > 1):
            User.objects.all().update(phase=current_phase-1)
        # to reset
        # User.objects.all().update(phase=1)
        return redirect('planners:currentphase')


@method_decorator([login_required, planner_required, finalisation_required], name='dispatch')
class RevertToPhase1(View):

    def get(self, request, *args, **kwargs):
        # delete all Preferences objects
        Preferences.objects.filter(first_name="Parry").delete()
        # delete all Lessons objects
        #  !!!!!!!

        current_phase = self.request.user.phase
        # rever phase to phase 1
        if (current_phase == 3):
            User.objects.all().update(phase=1)
        return redirect('planners:currentphase')


@login_required
@planner_required
def csv_upload(request):
    template = "classroom/planners/phaser_upload.html"

# course_Name, pillar_Type, event_Name, description, date, start_Time, event_Duration, lecturer,
# class_enrolled, location, is_event, initiated_by,
# is_conflicting, day_of_week

# 'Course Name', "Pillar", "Event Name", "Description", "Date", "Start Time", "Event Duration",
# "Lecturer", "Class Enrolled", "Location", "Initiated By", 'Day of Week'

    if request.method == "GET":
        return render(request, template)

    try:
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "This file is not a .csv file")
            raise Exception('not a csv file')

        # if file is too large
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
                csv_file.size/(1000*1000),))
            raise Exception('File too big')

        data_set = csv_file.read().decode('utf-8')
        io_string = io.StringIO(data_set)
        next(io_string)         # skip first line
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Schedule.objects.update_or_create(
                course_Name=column[0],
                pillar_Type=column[1],
                event_Name=column[2],
                description=column[3],
                date=column[4],
                start_Time=column[5],
                event_Duration=column[6],
                lecturer=column[7],
                class_Enrolled=column[8],
                location=column[9],
                is_Event=False,
                initiated_By=column[10],
                is_Conflicting=False,
                day_Of_Week=column[11],
            )

        context = {}
        messages.success(request, 'File upload successful')
        return render(request, template, context)

    except Exception as e:
        messages.error(request, "Unable to upload file. " + repr(e))
        messages.error(
            request, "Unable to upload file! Check your format and for empty rows!")
        return HttpResponseRedirect(reverse("planners:uploaddata"))


@method_decorator([login_required, planner_required, drafting_required], name='dispatch')
class AcceptSuggestionsListView(ListView):
    template_name = "classroom/planners/approve_list.html"

    def get_queryset(self):
        # returns Preferences submited by the current User
        return Schedule.objects.filter(is_Approved=True)


@method_decorator([login_required, planner_required, drafting_required], name='dispatch')
class AcceptSuggestion(UpdateView):
    model = Schedule
    template_name = "classroom/planners/approve_update.html"
    fields = ['is_Suggestion']

    def form_valid(self, form):
        details = form.save(commit=False)
        details.course_Name = self.object.course_Name
        details.pillar_Type = self.object.pillar_Type
        details.event_Name = self.object.event_Name
        details.lecturer = self.object.lecturer
        details.class_Enrolled = self.object.class_Enrolled
        details.description = self.object.description
        details.date = self.object.date
        details.start_Time = self.object.start_Time
        details.location = self.object.location
        details.event_Duration = self.object.event_Duration
        details.is_Event = self.object.is_Event
        details.initiated_By = self.object.initiated_By
        details.day_Of_Week = self.object.day_Of_Week
        details.save()
        return redirect('planners:acceptlist')

    def get_queryset(self):
        # only allow current User to edit the details he has submitted
        return Schedule.objects.filter(is_Approved=True)


@method_decorator([login_required, planner_required, drafting_required], name='dispatch')
class FinaliseView(View):

    def get(self, request, *args, **kwargs):
        Schedule.objects.filter(is_Suggestion=True).update(is_Finalised=True)
        return redirect('planners:home')


@method_decorator([login_required, planner_required, finalisation_required], name='dispatch')
class FinalisedCalendarView(View):
    model = Schedule
    template_name = 'classroom/planners/final_calendar.html'

    def get_context_data(self, **kwargs):
        context = super(ViewDraftCalendar, self).get_context_data(**kwargs)
        objects = Schedule.objects.all()
        user = self.request.user
        phase = self.request.user.phase
        context['jsonset'] = serializers.serialize("json", objects)
        # context['phase'] = phase
        # context['user'] = user
        # context['userdata'] = serializers.serialize("json", user)
        # context['jsonphase'] = serializers.serialize("json", phase)
        return context

from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect

from icalendar import Calendar, Event, LocalTimezone
from datetime import datetime, timedelta
from random import randint
from sys import exit
from os.path import expanduser,isdir
import csv
from .convert import Convert

usertypes = { 
    'professor': 1, 
    'sutdadmin': 2, 
    'coursecoordinators': 3, 
    'timetableplanner': 4, 
    'student' : 5
    }    

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == usertypes['professor']:
            return redirect('professors:professor_main')
        elif request.user.user_type == usertypes['coursecoordinators']:
        	return redirect('coordinators:coordinator_main')
        elif request.user.user_type == usertypes['timetableplanner']:
            return redirect('planners:planner_main')
        elif request.user.user_type == usertypes['sutdadmin']:
            return redirect('sutdadmin:sutdadmin_main')
        else:
            return redirect('students:student_main')
    return render(request, 'classroom/home.html')

class ForbiddenView(TemplateView):
    template_name = '403.html'

class ICSConverterView(View):

    def get(self, request, *args, **kwargs):
        # response = HttpResponse(content_type='text/calendar')
        # response['Content-Disposition'] = 'attachment; filename="calendar.ics"'

        with open('csvtoics.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            header = ["Subject", "Start Date", "Start Time", "End Date", "End Time", "All Day Event", "Description", "Location", "Private"]
            writer.writerow(header)
            writer.writerow(["50.001", "20190424T083000", "08:30", "20190424T103000", "10:00", "FALSE", "Describe this", "Lecture Theatre", "TRUE"])

        csvFile.close()

        convert = Convert()
        convert.CSV_FILE_LOCATION = 'csvtoics.csv'
        convert.SAVE_LOCATION = 'saved.ics'
        convert.HEADER_COLUMNS_TO_SKIP = 1
        convert.NAME = 0
        convert.START_DATE = 1
        convert.START_TIME = 2
        convert.END_DATE = 3
        convert.END_TIME = 4
        convert.DESCRIPTION = 6
        convert.LOCATION = 7

        convert.read_csv()
            
        convert.make_ical()
        convert.save_ical()
        with open('saved.ics', 'r') as fh:
            response = HttpResponse(fh.read(), content_type='text/calendar')
            response['Content-Disposition'] = 'attachment; filename="calendar.ics"'
        

        return response



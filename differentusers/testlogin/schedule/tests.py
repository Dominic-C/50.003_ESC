from django.test import TestCase
from schedule.models import Schedule
import datetime
from django.urls import reverse, reverse_lazy

# Create your tests here.
class ScheduleTestCase(TestCase):
    def setUp(self):
        Schedule.objects.create(title = "50.005 CSE", date = "2019-03-31", start_time = "09:00", end_time = "10:30", lecturer = "Prof David", location = "2.506")

    def test_successfully_created(self):
        check = Schedule.objects.get(title = "50.005 CSE")
        # get field value
        test_start_time = getattr(check, "start_time")
        test_end_time = getattr(check, "end_time")
        test_assigned_prof = getattr(check, "lecturer")
        test_location = getattr(check, "location")

        self.assertEqual(test_start_time, datetime.time(9,0)) # hours, minutes
        self.assertEqual(test_end_time, datetime.time(10,30))
        self.assertEqual(test_assigned_prof, "Prof David")
        self.assertEqual(test_location, "2.506")

    def test_create_schedule_form_valid(self):
        form_data = {'title' : "10.009 Digital World", 'date': "2019-03-31",'start_time' : "09:00", 'end_time' : "10:30", "lecturer" : "Prof Oka", "location" : "2.506"}
        response = self.client.post(reverse("schedule:create"), form_data)
        self.assertEqual(Schedule.objects.last().title, "10.009 Digital World")
        self.assertEqual(Schedule.objects.last().lecturer, "Prof Oka")

    # Form is invalid so it is not saved in Schedule Database
    def test_create_schedule_form_invalid_title(self):
        form_data = {'start_time' : "09:00", 'end_time' : "10:30", "lecturer" : "Prof Oka2", "location" : "2.506"}
        response = self.client.post(reverse("schedule:create"), form_data)
        self.assertEqual(Schedule.objects.last().title, "50.005 CSE")
        self.assertEqual(Schedule.objects.last().lecturer, "Prof David")

    # Form is invalid so it is not saved in Schedule Database
    def test_create_schedule_form_invalid_starttime(self):
        form_data = {'title' : "10.009 Digital World", 'end_time' : "10:30", "lecturer" : "Prof Oka2", "location" : "2.506"}
        response = self.client.post(reverse("schedule:create"), form_data)
        self.assertEqual(Schedule.objects.last().title, "50.005 CSE")
        self.assertEqual(Schedule.objects.last().lecturer, "Prof David")

    # Form is invalid so it is not saved in Schedule Database
    def test_create_schedule_form_invalid_endtime(self):
        form_data = {'title' : "10.009 Digital World", 'start_time' : "09:00", "lecturer" : "Prof Oka2", "location" : "2.506"}
        response = self.client.post(reverse("schedule:create"), form_data)
        self.assertEqual(Schedule.objects.last().title, "50.005 CSE")
        self.assertEqual(Schedule.objects.last().lecturer, "Prof David")

    # Form is invalid so it is not saved in Schedule Database
    def test_create_schedule_form_invalid_lecturer(self):
        form_data = {'title' : "10.009 Digital World", 'start_time' : "09:00", 'end_time' : "10:30", "location" : "2.506"}
        response = self.client.post(reverse("schedule:create"), form_data)
        self.assertEqual(Schedule.objects.last().title, "50.005 CSE")
        # self.assertEqual(Schedule.objects.last().lecturer, "Prof David")

    # Form is invalid so it is not saved in Schedule Database
    def test_create_schedule_form_invalid_location(self):
        form_data = {'title' : "10.009 Digital World", 'start_time' : "09:00", 'end_time' : "10:30", "lecturer" : "Prof Oka2"}
        response = self.client.post(reverse("schedule:create"), form_data)
        self.assertEqual(Schedule.objects.last().title, "50.005 CSE")
        self.assertEqual(Schedule.objects.last().lecturer, "Prof David")

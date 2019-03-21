from django.test import TestCase
from schedule.models import Schedule
import datetime

# Create your tests here.
class ScheduleTestCase(TestCase):
    def setUp(self):
        Schedule.objects.create(title = "50.005 CSE", start_time = "09:00", end_time = "10:30", lecturer = "Prof David", location = "2.506")

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

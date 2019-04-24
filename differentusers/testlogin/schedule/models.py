from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, validate_comma_separated_integer_list
import datetime

usertypes = {
    'professor': 1,
    'sutdadmin': 2,
    'coursecoordinators': 3,
    'timetableplanner': 4,
    'student': 5
}
HOUR_CHOICES = [
    (datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(7, 24)]
DURATION_CHOICES = [(x, '{:02d}'.format(x*15)) for x in range(1, 13)]
DAY_CHOICES = [(x, x) for x in range(1, 8)]
PILLARS = ['ASD', 'ISTD', 'EPD', 'ESD', 'FRESHMORE', 'MASTERS', 'PHD', "NONE"]
PILLAR_CHOICES = [(PILLARS[x], PILLARS[x]) for x in range(len(PILLARS))]
LOCATION_CHOICES = [(1, 'any'), (2, 'Lecture Theatre')]


class Schedule(models.Model):
    course_Name = models.CharField(max_length=120)
    pillar_Type = models.CharField(max_length=10, choices=PILLAR_CHOICES)
    event_Name = models.CharField(max_length=120, default="None")
    description = models.TextField(blank=True, null=True)
    date = models.DateField(("Date"), default=datetime.date.today)
    start_Time = models.TimeField()
    event_Duration = models.IntegerField(default=0, choices=DURATION_CHOICES)
    lecturer = models.CharField(max_length=50)
    class_Enrolled = models.CharField(max_length=4, default="")
    location = models.IntegerField()
    is_Suggestion = models.BooleanField(default=False)
    is_Finalized = models.BooleanField(default=False)

    is_Event = models.BooleanField(default=False)
    initiated_By = models.CharField(max_length=50, default="Nobody")
    is_Conflicting = models.BooleanField(default=False)
    is_classconflict = models.BooleanField(default=False)
    is_profconflict = models.BooleanField(default=False)
    day_Of_Week = models.IntegerField(
        default=1, validators=[MaxValueValidator(7), MinValueValidator(1)])

    def __str__(self):
        return "{} for {}".format(self.course_Name, self.class_Enrolled)

# class NewSchedule(models.Model):
    # title = models.CharField(max_length=120)
    # pillarType = models.CharField(max_length=10)
    # scheduleID = models.IntegerField()
    # eventName = models.CharField(max_length=120)
    # description = models.TextField(blank=True, null=True)
    # date = models.DateField(("Date"), default=datetime.date.today)
    # start_time = models.TimeField()
    # end_time = models.TimeField()
    # lecturer = models.CharField(max_length=50)
    # classEnrolled = models.CharField(max_length=4)
    # location = models.CharField(max_length=50)
    # isEvent = models.BooleanField(default=False)
    # initiatedBy = models.IntegerField()


#     def __str__(self):
#         return self.title

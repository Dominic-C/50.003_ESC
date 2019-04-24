from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, validate_comma_separated_integer_list
import datetime

# Create your models here.

usertypes = {
    'professor': 1,
    'sutdadmin': 2,
    'coursecoordinators': 3,
    'timetableplanner': 4,
    'student': 5
}
HOUR_CHOICES = [
    (datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(7, 24)]
DURATION_CHOICES = [(x*15, '{:02d}'.format(x*15)) for x in range(1, 13)]
DAY_CHOICES = [(x, x) for x in range(1, 8)]
PILLARS = ['ASD', 'ISTD', 'EPD', 'ESD', 'FRESHMORE', 'MASTERS', 'PHD', 'NIL']
PILLAR_CHOICES = [(x, PILLARS[x]) for x in range(len(PILLARS))]
LOCATION_CHOICES = [('1', 'any'), ('2', 'Lecture Theatre')]

"""

"""


class Schedule(models.Model):
    course_Name = models.CharField(max_length=120)
    pillar_Type = models.IntegerField(max_length=10, choices=PILLAR_CHOICES)

    event_Name = models.CharField(max_length=120, default="None")
    lecturer = models.CharField(max_length=50)
    class_Enrolled = models.CharField(max_length=6, default="")

    description = models.TextField(blank=True, null=True)
    date = models.DateField(("Date"), default=datetime.date.today)
    start_Time = models.TimeField()
    event_Duration = models.IntegerField(default=0, choices=DURATION_CHOICES)
    location = models.IntegerField()
    is_Event = models.BooleanField(default=False)
    initiated_By = models.CharField(max_length=50, default="Nobody")
    is_Conflicting = models.BooleanField(default=False)

    day_Of_Week = models.IntegerField(
        default=1, validators=[MaxValueValidator(7), MinValueValidator(1)])

    def __str__(self):
        return self.pillar_Type + " - " + self.course_Name

    def __iter__(self):
        for field_name in self._meta.get_all_field_names():
            value = getattr(self, field_name, None)
            yield (field_name, value)

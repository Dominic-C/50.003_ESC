from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, validate_comma_separated_integer_list
import datetime

# Create your models here.


class Schedule(models.Model):
    course_Name = models.CharField(max_length=120)
    pillar_Type = models.CharField(max_length=10, default="Freshmore")
    schedule_ID = models.IntegerField()
    event_Name = models.CharField(max_length=120, default="None")
    description = models.TextField(blank=True, null=True)
    date = models.DateField(("Date"), default=datetime.date.today)
    start_Time = models.TimeField()
    event_Duration = models.IntegerField(default=0)
    lecturer = models.CharField(max_length=50)
    class_Enrolled = models.CharField(max_length=4, default="None")
    location = models.CharField(max_length=50)
    is_Event = models.BooleanField(default=False)
    initiated_By = models.CharField(max_length=50, default="Nobody")
    is_Conflicting = models.BooleanField(default=False)
    day_Of_Week = models.IntegerField(
        default=1, validators=[MaxValueValidator(7), MinValueValidator(1)])

    def __str__(self):
        return self.course_Name

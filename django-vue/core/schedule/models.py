from django.db import models
import datetime

# Create your models here.
class Schedule(models.Model):
    title = models.CharField(max_length=120)
    pillarType = models.CharField(max_length=10, default="Freshmore")
    scheduleID = models.IntegerField()
    eventName = models.CharField(max_length=120, default="None")
    description = models.TextField(blank=True, null=True)
    date = models.DateField(("Date"), default=datetime.date.today)
    start_time = models.TimeField()
    eventDuration = models.IntegerField(default=0)
    lecturer = models.CharField(max_length=50)
    classEnrolled = models.CharField(max_length=4, default="None")
    location = models.CharField(max_length=50)
    isEvent = models.BooleanField(default=False)
    initiatedBy = models.CharField(max_length=50, default="Nobody")

    def __str__(self):
        return self.title
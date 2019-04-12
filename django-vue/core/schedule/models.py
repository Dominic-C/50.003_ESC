from django.db import models
import datetime

# Create your models here.
class Schedule(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(("Date"), default=datetime.date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lecturer = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    isEvent = models.BooleanField(default=False)

    def __str__(self):
        return self.title
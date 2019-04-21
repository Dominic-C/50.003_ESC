from django.db import models
import datetime

# Create your models here.
# class Schedule(models.Model):
#     title = models.CharField(max_length=120)
#     description = models.TextField(blank=True, null=True)
#     date = models.DateField(("Date"), default=datetime.date.today)
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     lecturer = models.CharField(max_length=50)
#     location = models.CharField(max_length=50)
#     isEvent = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title

class Schedule(models.Model):
    title = models.CharField(max_length=120)
    pillarType = models.CharField(max_length=10)
    scheduleID = models.IntegerField()
    eventName = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(("Date"), default=datetime.date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lecturer = models.CharField(max_length=50)
    classEnrolled = models.CharField(max_length=4)
    location = models.CharField(max_length=50)
    isEvent = models.BooleanField(default=False)
    initiatedBy = models.IntegerField()
    isConflicting = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
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
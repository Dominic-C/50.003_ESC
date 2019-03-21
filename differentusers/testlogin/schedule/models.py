from django.db import models

# Create your models here.
class Schedule(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lecturer = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
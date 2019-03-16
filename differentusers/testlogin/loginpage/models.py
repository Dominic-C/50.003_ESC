from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe

USER_TYPE_CHOICES = (
    (1, 'professor'),
    (2, 'sutdadmin'),
    (3, 'coursecoordinators'),
    (4, 'timetableplanner'),
    (5, 'student'),
)

class User(AbstractUser):
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=5)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Preferences(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='userpref')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=5)
    subject_code = models.CharField(max_length=10)
    subject_name = models.CharField(max_length=50)
    cohort_size = models.PositiveSmallIntegerField()
    cohort_num = models.PositiveSmallIntegerField()

    def __str__(self):
        string = "{} {}: {} {} | {} x {}".format(self.first_name, self.last_name, self.subject_code, 
            self.subject_name, self.cohort_size, self.cohort_num)
        return string

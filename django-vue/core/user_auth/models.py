from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, validate_comma_separated_integer_list
from django.utils.html import escape, mark_safe

USER_TYPE_CHOICES = (
    (1, 'professor'),
    (2, 'sutdadmin'),
    (3, 'coursecoordinators'),
    (4, 'timetableplanner'),
    (5, 'student'),
)

usertypes = { 
    'professor': 1, 
    'sutdadmin': 2, 
    'coursecoordinators': 3, 
    'timetableplanner': 4, 
    'student' : 5
    }

PHASE_CHOICES = (
    (1, 'Before First Draft'),
    (2, 'Drafting'),
    (3, 'Finalisation'),
)

class User(AbstractUser):
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=5)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phase = models.PositiveSmallIntegerField(choices=PHASE_CHOICES, default=1)

    def get_user_type(self):
        if self.user_type == usertypes['professor']:
            return 'Professor'
        elif self.user_type == usertypes['coursecoordinators']:
            return 'Course Coordinator'
        elif self.user_type == usertypes['sutdadmin']:
            return 'SUTD Admin'
        elif self.user_type == usertypes['timetableplanner']:
            return 'Timetable Planner'
        else:
            return 'Student'
            
    def get_phase(self):
        if self.phase == 1:
            return "Before First Draft"
        elif self.phase == 2:
            return "Drafting"
        elif self.phase == 3:
            return "Finalisation"
        else:
            return "None"


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
    cohort_size = models.PositiveSmallIntegerField(default=50, validators=[MaxValueValidator(800), MinValueValidator(1)])
    cohort_num = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(16), MinValueValidator(1)])

    def __str__(self):
        string = "{} {}: {} {} | {} x {}".format(self.first_name, self.last_name, self.subject_code, 
            self.subject_name, self.cohort_size, self.cohort_num)
        return string


class Lesson(models.Model):
    course_name = models.CharField(max_length=50)
    pillar = models.CharField(max_length=10)
    title = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    class_enrolled = models.CharField(max_length=10)
    day_of_week = models.CharField(max_length=20)
    duration = models.PositiveSmallIntegerField(default=90, validators=[MaxValueValidator(360), MinValueValidator(30)])

    def __str__(self):
        return "{} - {} for {}".format(self.course_name, self.title, self.class_enrolled) 
    
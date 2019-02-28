from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'professor'),
        (2, 'sutdadmin'),
        (3, 'coursecoordinators'),
        (4, 'timetableplanner'),
        (5, 'student'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=5)



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

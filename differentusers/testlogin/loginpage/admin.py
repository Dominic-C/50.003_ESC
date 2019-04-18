from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Preferences, Lesson
from schedule.models import NewSchedule


admin.site.register(User, UserAdmin)
admin.site.register(Preferences)
admin.site.register(Lesson)
admin.site.register(NewSchedule)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Preferences, Example
from schedule.models import Schedule


admin.site.register(User, UserAdmin)
admin.site.register(Preferences)
admin.site.register(Example)
admin.site.register(Schedule)
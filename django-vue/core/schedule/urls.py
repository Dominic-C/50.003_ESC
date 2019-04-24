from django.urls import include, path
from .views import *
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', ScheduleListView.as_view(), name='list'),
    path('testingdropdown', views.add_schedule, name='addschedule'),
    path('getical', views.save_ical, name="getical")
    path('edit', ScheduleEditView.as_view(), name='editsuggestion')
    path('conflicts', ScheduleConflictView.as_view(), name="viewconflict")
]

from django.urls import include, path
from schedule.views import ScheduleCreateView, ScheduleListView
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', ScheduleListView.as_view(), name='list'),
    path('create', ScheduleCreateView.as_view(), name='create'),
    path('testingdropdown', views.add_schedule, name = 'addschedule')
]
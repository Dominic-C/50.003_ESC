from django.urls import include, path
from .views import ScheduleCreateView, ScheduleListView
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', ScheduleListView.as_view(), name='list'),
    path('testingdropdown', views.add_schedule, name='addschedule'),
    # path('')
]

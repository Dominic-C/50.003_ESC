from django.urls import include, path
from schedule.views import ScheduleCreateView, ScheduleListView

app_name = 'schedule'

urlpatterns = [
    path('', ScheduleListView.as_view(), name='list'),
    path('create', ScheduleCreateView.as_view(), name='create'),
]
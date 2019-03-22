from django.urls import include, path
from schedule.views import ScheduleListView

urlpatterns = [
    path('', ScheduleListView.as_view()),
]
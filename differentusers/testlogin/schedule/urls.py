from django.urls import include, path
# from schedule.views import ScheduleListView
from . import views
from loginpage.views.classroom import home

app_name = 'schedule'

urlpatterns = [
    # path('', ScheduleListView.as_view(), name='list'),
    # path('create', ScheduleCreateView.as_view(), name='create'),
    path('testingdropdown', views.add_schedule, name = 'addschedule'),
    # path('serialized', views.serialized_schedule, name = 'serialize')
]

# urlpatterns = [
# 	path('', home, name='addschedule'),
# 	]
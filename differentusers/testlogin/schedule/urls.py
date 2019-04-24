from django.urls import include, path
# from schedule.views import ScheduleListView
from . import views
from loginpage.views.classroom import home

app_name = 'schedule'

urlpatterns = [
    path('testingdropdown', views.add_schedule, name = 'addschedule'),
    path('allschedules', views.ModifyScheduleListView.as_view() , name= 'allschedules'),
    path('modify/<int:pk>', views.ModifyScheduleEditView.as_view() , name= 'modify'),
    path('delete/<int:pk>', views.ModifyScheduleDeleteView.as_view() , name= 'delete')
]
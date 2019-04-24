from django.urls import include, path
from .views import ScheduleListView
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', ScheduleListView.as_view(), name='list'),
    path('testingdropdown', views.add_schedule, name='addschedule'),
    path('getical', views.save_ical, name="getical"),
    path('allschedules', views.ModifyScheduleListView.as_view(), name='allschedules'),
    path('modify/<int:pk>', views.ModifyScheduleEditView.as_view(), name='modify'),
    path('delete/<int:pk>', views.ModifyScheduleDeleteView.as_view(), name='delete'),
    path('viewdraft', views.ViewDraftCalendar.as_view(), name="viewdraft"),
    #     path('suggest/<int:pk>', ScheduleEditView.as_view(), name='suggestedits'),
    #     path('approve/<int:pk>', ScheduleApproveView.as_view(),
    #          name='approvesuggestion'),
    #     path('conflicts', ScheduleConflictView.as_view(), name="conflicts"),
]

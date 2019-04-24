from django.urls import include, path

from .views import classroom, students, professors, coordinators, planners, sutdadmin


urlpatterns = [
    path('', classroom.home, name='home'),
    path('403', classroom.ForbiddenView.as_view(), name='403'),
    path('icsconvert', classroom.ICSConverterView.as_view(), name="icsconvert"),

    path('students/', include(([
        path('', students.StudentMainView.as_view(), name='student_main'),
    ], 'classroom'), namespace='students')),

    path('professors/', include(([
        path('', professors.ProfessorMainView.as_view(), name='professor_main'),
        path('submitdetails', professors.SubmitCourseDetailsView.as_view(),
             name='submitdetails'),
        path('details', professors.DetailsListView.as_view(), name='details'),
        path('details/edit/<int:pk>',
             professors.DetailsEditView.as_view(), name='editdetails'),
        path('details/delete/<int:pk>',
             professors.DetailsDeleteView.as_view(), name='deletedetails'),

    ], 'classroom'), namespace='professors')),

    path('coordinators/', include(([
        path('', coordinators.CoordinatorMainView.as_view(),
             name='coordinator_main'),
        path('accounts', coordinators.CoordinatorAccountsListView.as_view(),
             name='accountlist'),
        path('suggest/<int:pk>', coordinators.ScheduleEditView.as_view(),
             name='suggestedits'),
        path('approve/<int:pk>', coordinators.ScheduleApproveView.as_view(),
             name='approvesuggestion'),
        path('conflicts', coordinators.ScheduleConflictView.as_view(), name="conflicts")
    ], 'classroom'), namespace='coordinators')),

    path('planners/', include(([
        path('', planners.PlannerMainView.as_view(), name='planner_main'),
        path('export', planners.PreferencesCSVExportView.as_view(), name="exportcsv"),
        path('upload', planners.csv_upload, name="uploaddata"),
        path('phase', planners.CurrentPhase.as_view(), name='currentphase'),
        path('nextphase', planners.NextPhase.as_view(), name="nextphase"),
        path('prevphase', planners.PreviousPhase.as_view(), name="prevphase"),
        path('downloadsample', planners.SampleDownloadView.as_view(),
             name="downloadsample"),
        path('revert', planners.RevertToPhase1.as_view(), name="revert"),
        path('acceptlist', planners.AcceptSuggestionsListView.as_view(),
             name="acceptlist"),
        path('accept/<int:pk>', planners.AcceptSuggestion.as_view(), name="accept"),
        path('finalise', planners.FinaliseView.as_view(), name="finalise"),
        path('finalcalendar', planners.FinalisedCalendarView.as_view(),
             name="finalcalendar"),
    ], 'classroom'), namespace='planners')),

    path('sutdadmin/', include(([
        path('', sutdadmin.SutdAdminMainView.as_view(), name='sutdadmin_main'),
        path('makebooking', sutdadmin.MakeBookingView.as_view(), name='makebooking'),
        path('bookings', sutdadmin.BookingList.as_view(), name='bookings'),
        path('bookings/edit/<int:pk>',
             sutdadmin.EditBookingView.as_view(), name='editbooking'),
        path('bookings/delete/<int:pk>',
             sutdadmin.DeleteBookingView.as_view(), name='deletebooking'),
        path('bookings/viewcalendar',
             sutdadmin.AdminCalendarView.as_view(), name='viewcalendar'),
    ], 'classroom'), namespace='sutdadmin')),

]

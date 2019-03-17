from django.urls import include, path

from .views import classroom, students, professors, coordinators

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('', students.StudentMainView.as_view(), name='student_main'),
    ], 'classroom'), namespace='students')),

    path('professors/', include(([
        path('', professors.ProfessorMainView.as_view(), name='professor_main'),
        path('submitdetails', professors.SubmitCourseDetailsView.as_view(), name='submitdetails'),
        path('details', professors.DetailsListView.as_view(), name='details'),
        path('details/edit/<int:pk>', professors.DetailsEditView.as_view(), name='editdetails'),

    ], 'classroom'), namespace='professors')),

    path('coordinators/', include(([
        path('', coordinators.CoordinatorMainView.as_view(), name='coordinator_main'),
    ], 'classroom'), namespace='coordinators')),
]

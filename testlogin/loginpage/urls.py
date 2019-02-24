from django.urls import include, path

from .views import classroom, students, professors

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('', students.StudentMainView.as_view(), name='student_main'),
    ], 'classroom'), namespace='students')),

    path('professors/', include(([
        path('', professors.ProfessorMainView.as_view(), name='professor_main'),
    ], 'classroom'), namespace='professors')),
]

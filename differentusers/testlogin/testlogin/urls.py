"""testlogin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include


from loginpage.views import classroom, students, professors, coordinators, planners, sutdadmin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loginpage.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/professor/', professors.ProfessorSignUpView.as_view(), name='professor_signup'),
    path('accounts/signup/coordinator/', coordinators.CoordinatorSignUpView.as_view(), name='coordinator_signup'),
    path('accounts/signup/planner/', planners.PlannerSignUpView.as_view(), name='planner_signup'),
    path('accounts/signup/sutdadmin/', sutdadmin.SutdAdminSignUpView.as_view(), name='sutdadmin_signup'),
    path('schedule/', include('schedule.urls')),
]

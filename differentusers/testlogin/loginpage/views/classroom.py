from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return redirect('teachers:professor_main')
        else:
            return redirect('students:student_main')
    return render(request, 'classroom/home.html')

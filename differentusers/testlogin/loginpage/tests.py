from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from loginpage.models import Student, User, Preferences
from loginpage.forms import ProfessorSignUpForm, SubmitCourseDetails, StudentSignUpForm

usertypes = { 
    'professor': 1, 
    'sutdadmin': 2, 
    'coursecoordinators': 3, 
    'timetableplanner': 4, 
    'student' : 5
    }    


class PreferencesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(user_type=usertypes['professor'], first_name="Bob", last_name="Lee",
        	username="bob", password="sutd1234")
        cls.pref = Preferences.objects.create(created_by=cls.user, first_name=cls.user.first_name, 
        	last_name=cls.user.last_name, user_type=cls.user.user_type, subject_code="50.005", 
        	subject_name="CSE", cohort_size=50, cohort_num=9)

    def test_preferences_str(self):
    	self.assertEqual(str(self.pref), "Bob Lee: 50.005 CSE | 50 x 9")


class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(user_type=usertypes['student'], first_name="Barry", last_name="Allen",
        	username="barry", password="sutd1234")
        cls.student = Student.objects.create(user=cls.user)

    def test_student_str(self):
    	self.assertEqual(str(self.student), "barry")

# class PreferencesFormTest(TestCase):
#     def test_preferences_form(self):
#         form = RenewBookForm()
#         self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'renewal date')

#     def test_renew_form_date_field_help_text(self):
#         form = RenewBookForm()
#         self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from loginpage.models import Student, User, Preferences
from loginpage.forms import ProfessorSignUpForm, SubmitCourseDetails, StudentSignUpForm
from django.urls import reverse, reverse_lazy

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

class PreferencesFormTest(TestCase):
    def test_preferences_form_label(self):
        form = SubmitCourseDetails()
        self.assertEqual(form.fields['subject_code'].label, "Subject code")
        self.assertEqual(form.fields['subject_name'].label, "Subject name")
        self.assertEqual(form.fields['cohort_size'].label, "Cohort size")
        self.assertEqual(form.fields['cohort_num'].label, "Cohort num")
        
    
    def test_preferences_form_empty_cohortnum_field(self):
    	form = SubmitCourseDetails(data={'subject_code': "50.005", 'subject_name' : "CSE",
    		'cohort_size': 50}) 
    	self.assertFalse(form.is_valid())

    def test_preferences_form_empty_cohortsize_field(self):
    	form = SubmitCourseDetails(data={'subject_code': "50.005", 'subject_name' : "CSE",
    		'cohort_num': 10}) 
    	self.assertFalse(form.is_valid())

    def test_preferences_form_empty_subjectcode_field(self):
    	form = SubmitCourseDetails(data={'subject_name' : "CSE", 'cohort_num': 10,
    		'cohort_size': 50}) 
    	self.assertFalse(form.is_valid())

    def test_preferences_form_empty_subjectname_field(self):
    	form = SubmitCourseDetails(data={'subject_code': "50.005",'cohort_size': 50 ,
    		'cohort_num': 10}) 
    	self.assertFalse(form.is_valid())

    def test_preferences_form_valid(self):
    	user = User.objects.create_user(user_type=usertypes['professor'], first_name="Bob", last_name="Lee",
        	username="bob", password="sutd1234")
    	form = SubmitCourseDetails(data={'subject_code': "50.005", 'subject_name' : "CSE",
    		'cohort_size': 50, 'cohort_num': 9, 'created_by': user, 'first_name':user.first_name,
    		'last_name': user.last_name, 'user_type':user.user_type}) 

    	self.assertTrue(form.is_valid())


class HomePageTests(TestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)


class PermissionTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(user_type=usertypes['professor'], first_name="Bob", last_name="Lee",
        	username="bob", password="sutd1234")
        cls.pref = Preferences.objects.create(created_by=cls.user, first_name=cls.user.first_name, 
        	last_name=cls.user.last_name, user_type=cls.user.user_type, subject_code="50.005", 
        	subject_name="CSE", cohort_size=50, cohort_num=9)

	# students/
    def test_student_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('students:student_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_professor_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('professors:professor_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_coordinator_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('coordinators:coordinator_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_professor_details_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('professors:details'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_professor_submitdetails_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('professors:submitdetails'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_professor_editdetails_wo_pk_redirect_if_not_logged_in(self):
        response = self.client.get('/professors/details/edit')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 404)

    def test_professor_editdetails_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('professors:editdetails', kwargs={'pk': self.pref.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))


# test preferences form submit

# test preferences form edit

# test queryset (models)



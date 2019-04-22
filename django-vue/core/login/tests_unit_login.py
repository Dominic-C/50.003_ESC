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
        cls.profuser = User.objects.create_user(user_type=usertypes['professor'], first_name="Bob", last_name="Lee",
            username="prof", password="sutd1234")
        cls.pref = Preferences.objects.create(created_by=cls.profuser, first_name=cls.profuser.first_name, 
            last_name=cls.profuser.last_name, user_type=cls.profuser.user_type, subject_code="50.005", 
            subject_name="CSE", cohort_size=50, cohort_num=9)
        cls.studentuser = User.objects.create_user(user_type=usertypes['student'], first_name="Barry", last_name="Lee",
            username="student", password="sutd1234")
        cls.coorduser = User.objects.create_user(user_type=usertypes['coursecoordinators'], first_name="Babby", last_name="Lee",
            username="coord", password="sutd1234")
        cls.planneruser = User.objects.create_user(user_type=usertypes['timetableplanner'], first_name="Peppa", last_name="Chia",
            username="planner", password='sutd1234')

#===========================
# Tests -- Nobody Logged in
#===========================

    # students/
    def test_student_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('students:student_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/
    def test_professor_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('professors:professor_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # coordinators/
    def test_coordinator_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('coordinators:coordinator_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/details
    def test_professor_details_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('professors:details'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/submitdetails
    def test_professor_submitdetails_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('professors:submitdetails'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/details/edit ERROR
    def test_professor_editdetails_wo_pk_redirect_if_not_logged_in(self):
        response = self.client.get('/professors/details/edit')
        self.assertEqual(response.status_code, 404)

    # professors/details/edit/<int id>
    def test_professor_editdetails_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('professors:editdetails', kwargs={'pk': self.pref.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/
    def test_planner_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("planners:planner_main"))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/export
    def test_planner_export_redirect_if_not_logged_in(self):
        response = self.client.get('/planners/export')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/upload
    def test_planner_upload_redirect_if_not_logged_in(self):
        response = self.client.get('/planners/upload')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/phase
    def test_planner_phase_redirect_if_not_logged_in(self):
        response = self.client.get('/planners/phase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/nextphase
    def test_planner_nextphase_redirect_if_not_logged_in(self):
        response = self.client.get('/planners/nextphase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/prevphase
    def test_planner_prevphase_redirect_if_not_logged_in(self):
        response = self.client.get('/planners/prevphase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

#===========================
# Tests -- Prof Logged in
#===========================


    # professors/
    def test_professor_if_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get(reverse('professors:professor_main'))
        # status = 200
        self.assertEqual(response.status_code, 200)

    # professors/details
    def test_professor_details_if_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get(reverse('professors:details'))
        # status = 200
        self.assertEqual(response.status_code, 200)

    # professors/submitdetails
    def test_professor_submitdetails_if_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get(reverse('professors:submitdetails'))
        # status = 200
        self.assertEqual(response.status_code, 200)

    # professors/details/edit ERROR
    def test_professor_editdetails_wo_pk_if_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get('/professors/details/edit')
        # No such url, get status code = 404
        self.assertEqual(response.status_code, 404)

    # professors/details/edit/<int id>
    def test_professor_editdetails_if_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get(reverse('professors:editdetails', kwargs={'pk': self.pref.pk}))
        # status code = 200
        self.assertEqual(response.status_code, 200)

    # students/
    def test_student_redirect_if_prof_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get(reverse('students:student_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # coordinators/
    def test_coordinator_redirect_if_prof_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get(reverse('coordinators:coordinator_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/
    def test_planner_redirect_if_prof_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get(reverse("planners:planner_main"))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/export
    def test_planner_export_redirect_if_prof_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get('/planners/export')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/upload
    def test_planner_upload_redirect_if_prof_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get('/planners/upload')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/phase
    def test_planner_phase_redirect_if_prof_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get('/planners/phase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/nextphase
    def test_planner_nextphase_redirect_if_prof_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get('/planners/nextphase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/prevphase
    def test_planner_prevphase_redirect_if_prof_logged_in(self):
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get('/planners/prevphase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))


#===========================
# Tests -- Student Logged in
#===========================

    # professors/
    def test_professor_redirect_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get(reverse('professors:professor_main'))
        # redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/details
    def test_professor_details_redirect_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get(reverse('professors:details'))
        # redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/submitdetails
    def test_professor_submitdetails_redirect_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get(reverse('professors:submitdetails'))
        # redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/details/edit ERROR
    def test_professor_editdetails_wo_pk_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get('/professors/details/edit')
        # No such url, get status code = 404
        self.assertEqual(response.status_code, 404)

    # students/
    def test_student_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get(reverse('students:student_main'))
        # status code = 200
        self.assertEqual(response.status_code, 200)

    # coordinators/
    def test_coordinator_redirect_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get(reverse('coordinators:coordinator_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/
    def test_planner_redirect_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get(reverse("planners:planner_main"))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/export
    def test_planner_export_redirect_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get('/planners/export')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/upload
    def test_planner_upload_redirect_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get('/planners/upload')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/phase
    def test_planner_phase_redirect_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get('/planners/phase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/nextphase
    def test_planner_nextphase_redirect_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get('/planners/nextphase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/prevphase
    def test_planner_prevphase_redirect_if_student_logged_in(self):
        login = self.client.login(username='student', password='sutd1234')
        response = self.client.get('/planners/prevphase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))


#================================
# Tests -- Coordinator Logged in
#================================

    # professors/
    def test_professor_redirect_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get(reverse('professors:professor_main'))
        # redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/details
    def test_professor_details_redirect_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get(reverse('professors:details'))
        # redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/submitdetails
    def test_professor_submitdetails_redirect_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get(reverse('professors:submitdetails'))
        # redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/details/edit ERROR
    def test_professor_editdetails_wo_pk_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get('/professors/details/edit')
        # No such url, get status code = 404
        self.assertEqual(response.status_code, 404)

    # students/
    def test_student_redirect_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get(reverse('students:student_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # coordinators/
    def test_coordinator_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get(reverse('coordinators:coordinator_main'))
        # status code = 200
        self.assertEqual(response.status_code, 200)

    # planners/
    def test_planner_redirect_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get(reverse("planners:planner_main"))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/export
    def test_planner_export_redirect_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get('/planners/export')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/upload
    def test_planner_upload_redirect_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get('/planners/upload')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/phase
    def test_planner_phase_redirect_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get('/planners/phase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    # planners/nextphase
    def test_planner_nextphase_redirect_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get('/planners/nextphase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/prevphase
    def test_planner_prevphase_redirect_if_coord_logged_in(self):
        login = self.client.login(username='coord', password='sutd1234')
        response = self.client.get('/planners/prevphase')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))


#================================
# Tests -- Planner Logged in
#================================
    # professors/
    def test_professor_redirect_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse('professors:professor_main'))
        # redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/details
    def test_professor_details_redirect_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse('professors:details'))
        # redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/submitdetails
    def test_professor_submitdetails_redirect_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse('professors:submitdetails'))
        # redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # professors/details/edit ERROR
    def test_professor_editdetails_wo_pk_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get('/professors/details/edit')
        # No such url, get status code = 404
        self.assertEqual(response.status_code, 404)

    # students/
    def test_student_redirect_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse('students:student_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # coordinators/
    def test_coordinator_redirect_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse('coordinators:coordinator_main'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # planners/
    def test_planner_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:planner_main"))
        # status code = 200
        self.assertEqual(response.status_code, 200)
    
    # planners/export
    def test_planner_export_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:exportcsv"))
        # status code = 200
        self.assertEqual(response.status_code, 200)

    # planners/upload
    def test_planner_upload_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:uploaddata"))
        # status code = 200
        self.assertEqual(response.status_code, 200)
    
    # planners/phase
    def test_planner_phase_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:currentphase"))
        # status code = 200
        self.assertEqual(response.status_code, 200)
    
    # planners/nextphase
    def test_planner_nextphase_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:nextphase"))
        # status code = 200
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == reverse('planners:currentphase'))

    # planners/prevphase
    def test_planner_prevphase_if_planner_logged_in(self):
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:prevphase"))
        # status code = 200
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == reverse('planners:currentphase'))




class PreferencesCreateTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.profuser = User.objects.create_user(user_type=usertypes['professor'], first_name="Bob", last_name="Lee",
            username="prof", password="sutd1234")
        cls.pref = Preferences.objects.create(created_by=cls.profuser, first_name=cls.profuser.first_name, 
            last_name=cls.profuser.last_name, user_type=cls.profuser.user_type, subject_code="50.005", 
            subject_name="CSE", cohort_size=50, cohort_num=9)

    def test_submit_course_details_valid(self):
        form_data = {'subject_code': '10.009', 'subject_name': 'Digital World', 'cohort_size': 49, 'cohort_num': 10}
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:submitdetails"), form_data)
        self.assertEqual(str(Preferences.objects.get(subject_code='10.009')), "Bob Lee: 10.009 Digital World | 49 x 10")

        # Form is invalid so it is not saved in Preferences Database
    def test_submit_course_details_invalid_subj_code(self):
        form_data = {'subject_name': 'Digital World', 'cohort_size': 49, 'cohort_num': 10}
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:submitdetails"), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)

    # Form is invalid so it is not saved in Preferences Database
    def test_submit_course_details_invalid_subj_name(self):
        form_data = {'subject_code': '10.009', 'cohort_size': 49, 'cohort_num': 10}
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:submitdetails"), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)

    # Form is invalid so it is not saved in Preferences Database
    def test_submit_course_details_invalid_cohort_size(self):
        form_data = {'subject_code': '10.009', 'subject_name': 'Digital World', 'cohort_num': 10}
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:submitdetails"), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)

    # Form is invalid so it is not saved in Preferences Database
    def test_submit_course_details_invalid_cohort_num(self):
        form_data = {'subject_code': '10.009', 'subject_name': 'Digital World', 'cohort_size': 49}
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:submitdetails"), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)

    # Cohort_num should be less than 16
    # Form is invalid so it is not saved in Preferences Database
    def test_submit_course_details_edge_cohort_num(self):
        form_data = {'subject_code': '10.009', 'subject_name': 'Digital World', 'cohort_size': 49, 'cohort_num': 20}
        login  = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:submitdetails"), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)

    # Cohort_size should be less than 800
    # Form is invalid so it is not saved in Preferences Database
    def test_submit_course_details_edge_cohort_size(self):
        form_data = {'subject_code': '10.009', 'subject_name': 'Digital World', 'cohort_size': 900, 'cohort_num': 10}
        login  = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:submitdetails"), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)

    # subject_code length should be less than 10
    # Form is invalid so it is not saved in Preferences Database
    def test_submit_course_details_edge_subject_code(self):
        form_data = {'subject_code': '10.009XXXXXXXXX', 'subject_name': 'Digital World', 'cohort_size': 50, 'cohort_num': 10}
        login  = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:submitdetails"), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)

    # subject_name length should be less than 50
    # Form is invalid so it is not saved in Preferences Database
    def test_submit_course_details_edge_subject_code(self):
        form_data = {'subject_code': '10.009', 'subject_name': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'cohort_size': 50, 'cohort_num': 10}
        login  = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:submitdetails"), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)


class PreferencesEditTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.profuser = User.objects.create_user(user_type=usertypes['professor'], first_name="Bob", last_name="Lee",
            username="prof", password="sutd1234")
        cls.pref = Preferences.objects.create(created_by=cls.profuser, first_name=cls.profuser.first_name, 
            last_name=cls.profuser.last_name, user_type=cls.profuser.user_type, subject_code="50.005", 
            subject_name="CSE", cohort_size=50, cohort_num=9)

    # Submit a '50.005' course detail and edit it to '10.007', observe changes
    def test_edit_course_details(self):
        form_data = {'subject_code': '10.007', 'subject_name': 'Digital World', 'cohort_size': 49, 'cohort_num': 10}
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:editdetails", kwargs={'pk':self.__class__.pref.id}), form_data)
        self.assertEqual(self.__class__.pref.id, 1)
        self.assertEqual(str(Preferences.objects.filter(subject_code='10.007')[0]), "Bob Lee: 10.007 Digital World | 49 x 10")
        self.assertEqual(Preferences.objects.last().subject_code, "10.007")
        self.assertEqual(Preferences.objects.last().subject_name, "Digital World")
        self.assertEqual(Preferences.objects.last().cohort_size, 49)
        self.assertEqual(Preferences.objects.last().cohort_num, 10)

    # subject_code length should be less than 10
    # Form is invalid so it is not saved in Preferences Database
    def test_edit_course_details_edge_subject_code(self):
        form_data = {'subject_code': '10.009XXXXXXXXX', 'subject_name': 'Digital World', 'cohort_size': 49, 'cohort_num': 10}
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:editdetails", kwargs={'pk':self.__class__.pref.id}), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)

    # subject_name length should be less than 50
    # Form is invalid so it is not saved in Preferences Database
    def test_edit_course_details_edge_subject_name(self):
        form_data = {'subject_code': '10.009', 'subject_name': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'cohort_size': 49, 'cohort_num': 10}
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:editdetails", kwargs={'pk':self.__class__.pref.id}), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)

    # Cohort_num should be less than 16
    # Form is invalid so it is not saved in Preferences Database
    def test_edit_course_details_edge_cohort_num(self):
        form_data = {'subject_code': '10.009', 'subject_name': 'Digital World', 'cohort_size': 49, 'cohort_num': 20}
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:editdetails", kwargs={'pk':self.__class__.pref.id}), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)

    # Cohort_size should be less than 800
    # Form is invalid so it is not saved in Preferences Database
    def test_edit_course_details_edge_cohort_size(self):
        form_data = {'subject_code': '10.009', 'subject_name': 'Digital World', 'cohort_size': 900, 'cohort_num': 10}
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.post(reverse("professors:editdetails", kwargs={'pk':self.__class__.pref.id}), form_data)
        self.assertEqual(Preferences.objects.last().subject_code, "50.005")
        self.assertEqual(Preferences.objects.last().subject_name, "CSE")
        self.assertEqual(Preferences.objects.last().cohort_size, 50)
        self.assertEqual(Preferences.objects.last().cohort_num, 9)


class PhaseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(user_type=usertypes['timetableplanner'], first_name="Bob", last_name="Lee",
            username="planner", password="sutd1234")

    def test_next_phase(self):
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)
        # log the planner in to gain access
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:nextphase"))

        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 2)

    def test_next_phase_only_till_3(self):
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)
        # log the planner in to gain access
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:nextphase"))
        response = self.client.get(reverse("planners:nextphase"))
        response = self.client.get(reverse("planners:nextphase"))
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 3)


    def test_prev_phase(self):
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)
        # log the planner in to gain access
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:nextphase"))
        response = self.client.get(reverse("planners:prevphase"))
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)

    def test_prev_phase_always_bigger_than_0(self):
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)
        # log the planner in to gain access
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:prevphase"))
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)

    def test_phase_up_to_3_down_to_1(self):
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)
        # log the planner in to gain access
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:nextphase"))
        response = self.client.get(reverse("planners:nextphase"))
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 3)

        response = self.client.get(reverse("planners:prevphase"))
        response = self.client.get(reverse("planners:prevphase"))
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)

class PhasePermissionTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(user_type=usertypes['timetableplanner'], first_name="Bob", last_name="Lee",
            username="planner", password="sutd1234")
        cls.profuser = User.objects.create_user(user_type=usertypes['professor'], first_name="Bob", last_name="Lee",
            username="prof", password="sutd1234")


    def test_phase_1_permission(self):
        # assert that phase is 1 now
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)
        # log professor user in
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get(reverse('professors:details'), follow=True)
        # prof can access, status code = 200
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('professors:submitdetails'), follow=True)
        # prof can access, status code = 200
        self.assertEqual(response.status_code, 200)


    def test_phase_2_permission(self):
         # assert that phase is 1 now
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)

        # Log Planner user in
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:nextphase"))

        # assert that phase is 2 now
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 2)

        # Planner - Logout
        logout = self.client.logout()

        # Log Professor user in
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get(reverse('professors:details'), follow=True)

        # check that it returns 403: forbidden
        self.assertContains(response, 'Forbidden')
        response = self.client.get(reverse('professors:submitdetails'), follow=True)
        # check that it returns 403: forbidden
        self.assertEqual(response.status_code, 200)


    def test_phase_3_permission(self):
         # assert that phase is 1 now
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)

        # Log Planner user in
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:nextphase"))
        response = self.client.get(reverse("planners:nextphase"))

        # assert that phase is 3 now
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 3)

        # Planner - Logout
        logout = self.client.logout()

        # Log Professor user in
        login = self.client.login(username='prof', password='sutd1234')
        response = self.client.get(reverse('professors:details'), follow=True)

        # check that it returns 403: forbidden
        self.assertContains(response, 'Forbidden')
        response = self.client.get(reverse('professors:submitdetails'), follow=True)
        # check that it returns status code 200
        self.assertEqual(response.status_code, 200)
    

class RevertPhaseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(user_type=usertypes['timetableplanner'], first_name="Bob", last_name="Lee",
            username="planner", password="sutd1234")

    def test_revert_phase(self):
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)
        # log the planner in to gain access
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:nextphase"))
        response = self.client.get(reverse("planners:nextphase"))

        # assert that phase is 3 now
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 3)

        # revert phase to phase 1
        response = self.client.get(reverse("planners:revert"))
        self.__class__.user.refresh_from_db()

        # assert that phase is 1 now
        self.assertEqual(self.__class__.user.phase, 1)

    def test_revert_phase_phase_1(self):
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)
        # log the planner in to gain access
        login = self.client.login(username='planner', password='sutd1234')

        # try to revert
        response = self.client.get(reverse("planners:revert"), follow=True)
        # check that it returns 403: forbidden
        self.assertContains(response, 'Forbidden')
        logout = self.client.logout()

    def test_revert_phase_phase_2(self):
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 1)
        # log the planner in to gain access
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:nextphase"))

        # assert that phase is 2 now
        self.__class__.user.refresh_from_db()
        self.assertEqual(self.__class__.user.phase, 2)

        # try to revert
        response = self.client.get(reverse("planners:revert"), follow=True)

        # check that it returns 403: forbidden
        self.assertContains(response, 'Forbidden')
        logout = self.client.logout()

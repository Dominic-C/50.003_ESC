from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from loginpage.models import Student, User, Preferences


usertypes = { 
    'professor': 1, 
    'sutdadmin': 2, 
    'coursecoordinators': 3, 
    'timetableplanner': 4, 
    'student' : 5
    }

class MySeleniumTests(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.user = User.objects.create_user(user_type=usertypes['professor'], first_name="Bob", last_name="Lee",
        	username="bob", password="sutd1234")
		cls.selenium = WebDriver()
		cls.selenium.implicitly_wait(10)

	@classmethod
	def tearDownClass(cls):
		cls.selenium.quit()
		super().tearDownClass()

	def test_login(self):
		self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
		username_input = self.selenium.find_element_by_name("username")
		username_input.send_keys('bob')
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys('sutd1234')
		self.selenium.find_element_by_id("id_login").click()
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from loginpage.models import Student, User, Preferences
from schedule.models import Schedule
import time
from django.urls import reverse
from selenium.webdriver.support.ui import Select



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
        cls.planner = User.objects.create_user(user_type=usertypes['timetableplanner'], first_name="Tracy", last_name="Liu", username="planner", password="sutd1234")
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)



    def test_double_events(self):
        # initial log in as planner
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('planner')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('sutd1234')
        self.selenium.find_element_by_id("id_login").click()

        # find Before First Draft dropdown and click
        for a in self.selenium.find_elements_by_xpath('.//a'):
            # print(a.text)
            if(a.text == 'Before First Draft'):
                a.click()
                break

        self.selenium.implicitly_wait(10)
        self.selenium.find_element_by_xpath('//a[@href="/planners/phase"]').click()

        # find Next Phase button and click it. Click on yes when popup appears.
        for a in self.selenium.find_elements_by_xpath('//button'):
            # print(a.text)
            if(a.text == 'Next Phase'):
                a.click()
                self.selenium.implicitly_wait(5)
                self.selenium.find_element_by_xpath('//a[@href="/planners/nextphase"]').click()
                break
        
        # log out
        for a in self.selenium.find_elements_by_xpath('.//a'):
            # print(a.text)
            if(a.text == 'Log out'):
                a.click()
                break

        # log in
        for a in self.selenium.find_elements_by_xpath('.//a'):
            # print(a.text)
            if(a.text == 'Log in'):
                a.click()
                break

        # log in as bob
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('bob')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('sutd1234')
        self.selenium.find_element_by_id("id_login").click()

        # find Before First Draft dropdown and click
        for a in self.selenium.find_elements_by_xpath('.//a'):
            # print(a.text)
            if(a.text == 'After First Draft'):
                a.click()
                break

        self.selenium.implicitly_wait(10)
        self.selenium.find_element_by_xpath('//a[@href="/schedule/testingdropdown"]').click()

        courseName = self.selenium.find_element_by_id("id_course_Name")
        pillarType = Select(self.selenium.find_element_by_id("id_pillar_Type"))
        EventName = self.selenium.find_element_by_id("id_event_Name") # not used
        description = self.selenium.find_element_by_id("id_description")
        date = self.selenium.find_element_by_id("id_date")
        date.clear()
        classEnrolled = self.selenium.find_element_by_id("id_class_Enrolled")
        initiatedBy = self.selenium.find_element_by_id("id_initiated_By")
        initiatedBy.clear()
        dayOfWeek = self.selenium.find_element_by_id("id_day_Of_Week")
        dayOfWeek.clear()
        EventDuration = Select(self.selenium.find_element_by_id("id_event_Duration"))
        select_lecturer = Select(self.selenium.find_element_by_id('id_lecturer'))
        select_location = Select(self.selenium.find_element_by_id('id_location'))
        start_time = self.selenium.find_element_by_id("id_start_Time")
        

        # send keys to handlers
        pillarType.select_by_value('4')
        courseName.send_keys("50.003 Elements of Software Construction")
        pillarType.select_by_visible_text("ISTD")
        description.send_keys("Elements of software Construction is a term 5 module")
        date.send_keys("2019-03-21")
        # EventName.send_keys("Lecture")
        select_lecturer.select_by_value('1')
        select_location.select_by_value('1')
        start_time.send_keys("09:00")
        classEnrolled.send_keys("F01")
        initiatedBy.send_keys("Somebody") # should ideally be primary key of lecturer
        dayOfWeek.send_keys("2")

        self.selenium.find_element_by_xpath("//input[@type='submit']").click()


        # clear fields to prep for second submission

        courseName = self.selenium.find_element_by_id("id_course_Name")
        pillarType = Select(self.selenium.find_element_by_id("id_pillar_Type"))
        EventName = self.selenium.find_element_by_id("id_event_Name") # not used
        description = self.selenium.find_element_by_id("id_description")
        date = self.selenium.find_element_by_id("id_date")
        date.clear()
        classEnrolled = self.selenium.find_element_by_id("id_class_Enrolled")
        initiatedBy = self.selenium.find_element_by_id("id_initiated_By")
        initiatedBy.clear()
        dayOfWeek = self.selenium.find_element_by_id("id_day_Of_Week")
        dayOfWeek.clear()
        EventDuration = Select(self.selenium.find_element_by_id("id_event_Duration"))
        select_lecturer = Select(self.selenium.find_element_by_id('id_lecturer'))
        select_location = Select(self.selenium.find_element_by_id('id_location'))
        start_time = self.selenium.find_element_by_id("id_start_Time")

        courseName.clear()
        pillarType.select_by_value('0')
        description.clear()
        date.clear()
        classEnrolled.clear()
        initiatedBy.clear()
        dayOfWeek.clear()
        EventDuration.select_by_value('1')
        select_lecturer.select_by_value('1')
        initiatedBy.clear()
        dayOfWeek.clear()

        # send keys to handlers
        pillarType.select_by_value('4')
        courseName.send_keys("50.005 Computer System Engineering")
        pillarType.select_by_visible_text("ISTD")
        description.send_keys("Computer System Engineering is a term 5 module")
        date.send_keys("2019-03-22")
        # EventName.send_keys("Lecture")
        select_lecturer.select_by_value('1')
        select_location.select_by_value('2')
        start_time.send_keys("09:00")
        classEnrolled.send_keys("F01")
        initiatedBy.send_keys("Somebody") # should ideally be primary key of lecturer
        dayOfWeek.send_keys("2")

        self.selenium.find_element_by_xpath("//input[@type='submit']").click()

    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
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



    def test_login(self):
        # initial log in as planner
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('planner')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('sutd1234')
        self.selenium.find_element_by_id("id_login").click()

        # find Before First Draft dropdown and click
        for a in self.selenium.find_elements_by_xpath('.//a'):
            print(a.text)
            if(a.text == 'Before First Draft'):
                a.click()
                break

        self.selenium.implicitly_wait(10)
        self.selenium.find_element_by_xpath('//a[@href="/planners/phase"]').click()

        # find Next Phase button and click it. Click on yes when popup appears.
        for a in self.selenium.find_elements_by_xpath('//button'):
            print(a.text)
            if(a.text == 'Next Phase'):
                a.click()
                self.selenium.implicitly_wait(5)
                self.selenium.find_element_by_xpath('//a[@href="/planners/nextphase"]').click()
                break
        
        # log out
        for a in self.selenium.find_elements_by_xpath('.//a'):
            print(a.text)
            if(a.text == 'Log out'):
                a.click()
                break

        # log in
        for a in self.selenium.find_elements_by_xpath('.//a'):
            print(a.text)
            if(a.text == 'Log in'):
                a.click()
                break

        # log in as bob
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('bob')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('sutd1234')
        self.selenium.find_element_by_id("id_login").click()
        # self.selenium.find_element_by_xpath('//a[@href="/accounts/logout"]').click()
        # self.selenium.find_element_by_xpath('//a[@href="/accounts/login"]').click()

        # find Before First Draft dropdown and click
        for a in self.selenium.find_elements_by_xpath('.//a'):
            print(a.text)
            if(a.text == 'After First Draft'):
                a.click()
                break

        self.selenium.implicitly_wait(10)
        self.selenium.find_element_by_xpath('//a[@href="/schedule/testingdropdown"]').click()

        title = self.selenium.find_element_by_name("title")
        pillarType = self.selenium.find_element_by_name("pillarType")
        scheduleID = self.selenium.find_element_by_name("scheduleID")
        EventName = self.selenium.find_element_by_name("eventName")
        scheduleID = self.selenium.find_element_by_name("scheduleID")
        description = self.selenium.find_element_by_name("description")
        date = self.selenium.find_element_by_name("date")
        date.clear()


        title.send_keys("50.003 Elements of Software Construction")
        pillarType.send_keys("ISTD")
        scheduleID.send_keys("1000")
        description.send_keys("Elements of software Construction is a term 5 module")
        date.send_keys("2019-03-21")

        select_start = Select(self.selenium.find_element_by_id('id_start_time'))
        select_start.select_by_visible_text("09:00")

        select_end = Select(self.selenium.find_element_by_id('id_end_time'))
        select_end.select_by_visible_text("13:00")

        select_lecturer = Select(self.selenium.find_element_by_id('id_lecturer'))
        select_lecturer.select_by_value('1')






        

        # Planner - Logout
        # logout = self.client.logout()


        # Log Professor user in
        # login = self.client.login(username='bob', password='sutd1234')
        

        time.sleep(5)

        
    
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
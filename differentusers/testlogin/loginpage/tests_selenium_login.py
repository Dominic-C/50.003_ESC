from django.contrib.staticfiles.testing import StaticLiveServerTestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from loginpage.models import Student, User, Preferences
from schedule.models import Schedule

import csv
import random
import os

usertypes = { 
    'professor': 1, 
    'sutdadmin': 2, 
    'coursecoordinators': 3, 
    'timetableplanner': 4, 
    'student' : 5
    }

class MySeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(user_type=usertypes['professor'], first_name="Bob", last_name="Lee",
            username="bob", password="sutd1234")
        cls.planner = User.objects.create_user(user_type=usertypes['timetableplanner'], first_name="Tracy", last_name="Liu", username="planner", password="sutd1234")
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # cls.selenium.quit()
        super().tearDownClass()

    def test_upload_csv(self):
        # initial log in as planner
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('planner')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('sutd1234')
        self.selenium.find_element_by_id("id_login").click()

        # find Before First Draft dropdown and click
        for a in self.selenium.find_elements_by_xpath('.//a'):
            if(a.text == 'Before First Draft'):
                a.click()
                break

        # go to upload first draft
        self.selenium.implicitly_wait(10)
        self.selenium.find_element_by_xpath('//a[@href="/planners/upload"]').click()

        # assert that we are in the correct page
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/planners/upload' )

        # create the CSV file
        fuzzer = CSV_Fuzzer()
        fuzzer.csv_fuzzer(10)
        # find browse and click
        browse = self.selenium.find_element_by_class_name("custom-file-input")
        browse.send_keys(os.getcwd() + "/fuzzed_input.csv")

        # find upload and click
        for a in self.selenium.find_elements_by_xpath('.//button'):
            if(a.text == 'Upload'):
                a.click()

        alert = self.selenium.find_elements_by_class_name("alert-dismissible")
        self.assertEqual(alert.text, "File upload successful")



class CSV_Fuzzer:

	def csv_fuzzer(self, n):
		PILLARS = ['ASD', 'ISTD', 'EPD', 'ESD', 'FRESHMORE', 'MASTERS', 'PHD']
		COURSENAMES = ["50.001 Introduction to Information Systems & Programming", 
		"50.002 Computation Structures", "50.003 Elements of Software Construction", "50.004 Introduction to Algorithms",
		"50.005 Computer System Engineering", "50.034 Introduction to Probability and Statistics"]
		COURSENUMBER = ["50.001", "50.002", "50.003", "50.004", "50.005", "50.034"]

		with open('fuzzed_input.csv', 'w', newline='') as csvFile:
			writer = csv.writer(csvFile)
			header = ['Course Name', "Pillar", "Event Name", "Description", "Date", "Start Time", "Event Duration", "Lecturer", 
			"Class Enrolled", "Location", "Initiated By", 'Day of Week']
			writer.writerow(header)
			for i in range(n):
				row = []
				row.append(self.string_fuzz(random.choice(COURSENAMES)))
				row.append(random.choice(PILLARS))
				row.append(self.string_fuzz(random.choice(COURSENUMBER) + " Lecture"))
				row.append(self.string_fuzz("This is a lecture"))
				row.append(self.date_fuzz())
				row.append(self.time_fuzz())		#start_Time
				row.append("90")
				row.append(self.string_fuzz("Ngai Man"))
				row.append("F" + "0" + str(random.randint(1,9)))
				row.append("Lecture Theatre")
				row.append(self.string_fuzz("Ngai Man"))
				row.append(str(random.randint(1,7)))
				writer.writerow(row)
		csvFile.close()


	def date_fuzz(self):
		# sample: 2019-04-22
		string = '2019-'
		ls_months = ['01','02','03','04','05','06','07','08','09','10','11','12']
		ls_days = [str(i) if i>9 else "0"+str(i) for i in range(1,28)]
		string += ls_months[random.randint(0,len(ls_months)-1)]
		string += "-" + ls_days[random.randint(0,len(ls_days)-1)]
		return string

	def time_fuzz(self):
		ls_hours = [str(i) if i>9 else "0"+str(i) for i in range(8,19)]
		string = ""
		string += random.choice(ls_hours) + ":00"
		return string

	def integer_fuzz(self, range_count):
		return random.randint(1, range_count+1)

	def string_fuzz(self, line):
		choices = [self.string_swap]
		string = random.choice(choices)(line)
		return string

	def string_swap(self, line):
	#     This function takes in a line and choose a random index
	#     Then, swaps the letter at this index with the letter right after 
	    string = ""
	    if (len(line) > 1):
	        index = random.randint(0, len(line)-2)   # ignore the last letter
	        string = line[:index] + line[index+1] + line[index] + line[index+2:]
	        return string
	    else:
	        # if only one letter, return without swapping
	        return line
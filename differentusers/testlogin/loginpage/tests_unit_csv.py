from django.test import Client
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse, reverse_lazy
from schedule.models import Schedule
from loginpage.models import Student, User, Preferences

import csv
import random

usertypes = { 
    'professor': 1, 
    'sutdadmin': 2, 
    'coursecoordinators': 3, 
    'timetableplanner': 4, 
    'student' : 5
    }    

class UploadFuzzCSV(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(user_type=usertypes['timetableplanner'], first_name="Bob", last_name="Lee",
            username="planner", password="sutd1234")

    def test_upload_fuzz(self):
        self.assertEqual(len(Schedule.objects.all()), 0)
        # Log Planner user in
        login = self.client.login(username='planner', password='sutd1234')
        response = self.client.get(reverse("planners:uploaddata"))
        fuzzer = CSV_Fuzzer()
        fuzzer.csv_fuzzer(5)
        form_data = {'custom-file-input': 'fuzzed_input.csv'}
        
        response = self.client.post(reverse("planners:uploaddata"), form_data)

        # assert that contents have been imported into database
        # self.assertEqual(len(Schedule.objects.all()), 5)



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
                row.append(self.time_fuzz())        #start_Time
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

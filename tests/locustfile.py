from locust import HttpLocust, TaskSet, task, seq_task

# To run: locust --host=http://127.0.0.1:8000

def login(l):
    l.client.post("/accounts/login/", {"Username":"professor", "Password":"sutd1234"})

def logout(l):
    l.client.post("/accounts/logout/", {"username":"professor", "password":"sutd1234"} )

def index(l):
    l.client.get("/")


class UserBehavior(TaskSet):
    
    def on_start(self):
        self.login()

    def on_stop(self):
        self.logout()

    def logout(self):
        # login to the application
        response = self.client.get('/accounts/logout/')

    def login(self):
        # login to the application
        response = self.client.get('/accounts/login/')
        csrftoken = response.cookies['csrftoken']
        self.client.post('/accounts/login/',
                         {'username': 'planner', 'password': 'sutd1234'},
                         headers={'X-CSRFToken': csrftoken})

    @seq_task(1)
    def first_task(self):
        self.client.get("/")

    @seq_task(2)
    def second_task(self):
        self.client.get("/planners/")

    @seq_task(3)
    def third_task(self):
        self.client.get("/planners/phase")

    @seq_task(4)
    def fourth_task(self):
        self.client.get("/planners/upload")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
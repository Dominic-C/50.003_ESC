# Testing

## Project Files
The project files are found in the django-vue folder

## Tests
### Unit Tests
Found in the ```django-vue/core/schedule``` and ```django-vue/core/login folders``` \
To run the unit tests,
```$ python manage.py test --pattern="tests_unit_login.py" -v 2```

### System Tests
- Make sure you have Selenium installed, try ```$ pip install selenium```
- Run ```TestLogin.java```
- Run ```OpenTimeConflict.java```
- Run ```IntegrationTests.java```
- Run ```$ python manage.py test --pattern="tests_selenium.py"```

### Robustness Tests
1. Redirects regarding permissions & Brute-force Login\
Run ```RobustnessTesting.java```

2. Load Testing
- ```$ pip install locustio```
- Run django server
- ```cd``` to the folder containing ```locustfile.py```
- Run ```$ locust --host=http://127.0.0.1:8000```
- Once you've started Locust using the command lines, open up a browser and point it to ```http://localhost:8089/```
- Start load testing!

3. Fuzzer
- ```csv_fuzzer.py```

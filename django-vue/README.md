# 50.003_ESC

## Install required libraries

`pip3 install -r requirements.txt`
change directories to the `vue` subfolder
`npm install`

## Running
`cd` to the location of this folder \
`python manage.py makemigrations`\
`python manage.py migrate`\
`python manage.py runserver`\
If you run into any error (especially with regards to BruteBuster), try running `python manage.py migrate --run-syncdb` and pray\
go to 127.0.0.1:8000

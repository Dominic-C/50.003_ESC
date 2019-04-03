# 50.003_ESC

## Install required libraries
- Django
``pip3 install Django``
- crispyforms
``pip3 install --upgrade django-crispy-forms``
- brutebuster
``pip3 install django-brutebuster2``
- django rest framework
``pip3 install djangorestframework``

## Running
`cd` to the location of this folder \
`python manage.py makemigrations`\
`python manage.py migrate`\
`python manage.py runserver`\
If you run into any error (especially with regards to BruteBuster), try running `python manage.py migrate --run-syncdb` and pray\
go to 127.0.0.1:8000

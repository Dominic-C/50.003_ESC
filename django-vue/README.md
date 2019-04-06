# 50.003_ESC

## Install required libraries

Run `pip3 install -r requirements.txt`, or if that fails, try doing the following:

``pip3 install Django``
``pip3 install --upgrade django-crispy-forms``
``pip3 install django-brutebuster2``
``pip3 install djangorestframework``

## Running
`cd` to the location of this folder \
`python manage.py makemigrations`\
`python manage.py migrate`\
`python manage.py runserver`\
If you run into any error (especially with regards to BruteBuster), try running `python manage.py migrate --run-syncdb` and pray\
go to 127.0.0.1:8000

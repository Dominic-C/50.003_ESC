# core

> A Vue.js project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

## Running the Server

`cd` to the location of this folder (where manage.py is located)\
`python manage.py makemigrations`\
`python manage.py migrate`\
`python manage.py runserver`\
If you run into any error (especially with regards to BruteBuster), try running `python manage.py migrate --run-syncdb` and pray\
go to `127.0.0.1:8000`

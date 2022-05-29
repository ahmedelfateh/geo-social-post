<h1 align="center">  Geo Social Posts </h1>

[![Django](https://img.shields.io/badge/Django-3.2.13-blue)](https://github.com/django/django/tree/3.2.13)
[![Python](https://img.shields.io/badge/python-3.8.1-blue)](https://github.com/python/cpython/tree/v3.8.1)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)

## Basic Commands

### setup the development environment

1. [Install docker on you platform.](https://docs.docker.com/docker-for-windows/install/)
2. [Install docker-compose on your platform.](https://docs.docker.com/compose/install/)
3. Run the Development environment:

- create and launch the Project

```bash
    git clone https://github.com/ahmedelfateh/geo-social-post
    cd geo-social-post
    docker-compose up --build
```

4. Open another terminal tab, to migrate DB:

```bash
    docker-compose run --rm django ./manage.py migrate
```

### run development environment **Recurring Task** 🔃

```bash
    docker-compose up
```

> **HINT**: Be sure to run "docker-compose up --build" if any requirements changed or updated, run it with every pull any way.

### Setting Up Your Users

- To create an **superuser account**, start in the root folder and use this command:

```bash
    docker-compose run --rm django ./manage.py createsuperuser
```

### Testing

- Run tests, for all apps:

> **HINT**: To run tests, you need to change DEPLOYMENT env var to "TEST" for more clean test running

```bash
    docker-compose run --rm django ./manage.py test
```

### Code Quality / Style

```bash
    docker-compose run --rm django ./manage.py black .
    docker-compose run --rm django ./manage.py flake8
```

## Access App

- you can access the App Admin on [Admin](http://localhost:8000/admin)
- you can access swagger docs for API on [Swagger](http://localhost:8000/api/v1/swagger/)
- you can access the Celery Flower on (user:admin/pass:admin0) [Flower](http://localhost:5555)

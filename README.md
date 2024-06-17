# lunch-log
Office Lunch Receipt Management and Recommendation System

![lint](https://github.com/vkmrishad/lunch-log/actions/workflows/lint.yaml/badge.svg?branch=main)
![test](https://github.com/vkmrishad/lunch-log/actions/workflows/test.yaml/badge.svg?branch=main)
<a href="https://docs.astral.sh/ruff/"><img alt="Code style: ruff" src="https://img.shields.io/badge/code%20style-ruff-000000.svg"></a>

This system is build over s3 storage which is scalable and reliable.

## Clone

    git clone https://github.com/vkmrishad/lunch-log.git
    or
    git clone git@github.com:vkmrishad/lunch-log.git

## System dependencies

* [Python: 3.10+](https://www.python.org/downloads/)
* [PostgreSQL: 13+](https://www.postgresql.org/download/)
* [Redis: 6+](https://redis.io/docs/getting-started/installation/)
* [Minio (Simulate AWS S3)](https://min.io/download) - Only works with poetry (local development)

## Environment and Package Management
Install [Poetry](https://python-poetry.org/)

    $ pip install poetry
    or
    $ pip3 install poetry

Activate or Create Env

    $ poetry shell

Install Packages from Poetry

    $ poetry install

NB: When using virtualenv, install from [requirements.txt](/requirements.txt) using `$ pip install -r requirements.txt`.
For environment variables follow [sample.env](/sample.env)

## Runserver

    $ python manage.py runserver
    or
    $ ./manage.py runserver

## Run Celery

    $ celery -A lunch_log  worker -l info -B

## Runserver using docker
Check this documentation to run with [docker](https://docs.docker.com/desktop/), refer [link](https://docs.docker.com/samples/django/)
Create .env file in project folder and copy all ENV vars without having `export`.

For initial db setup add, postgres ENV vars
```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```
You can use your own values, Please use `DATABASE_HOST='postgres'` for docker settings only
    
    $ make build
    or 
    $ docker-compose build

    $ make up
    or 
    $ docker-compose up
    or 
    $ docker-compose up -d

For shutting down use,

    $ make down
    or 
    $ docker-compose down

Apply migration to database
    
    $ make migrate
    or 
    $ docker-compose exec app python manage.py migrate

Create superuser

    $ docker-compose exec app python manage.py createsuperuser


Testing

    $ docker-compose exec app moto_server &
    $ docker-compose exec app pytest

#### Access server: http://127.0.0.1:8000
#### Access Admin: http://127.0.0.1:8000/admin/

## API Endpoints
Run collect static to update swagger templates

    $ python manage.py collectstatic
    or
    $ ./manage.py collectstatic

Check Swagger/Redoc documantation after running server
#### Swagger: http://127.0.0.1:8000/api/swagger/
#### Redoc: http://127.0.0.1:8000/redoc/

## Authentication
Using take `csrf_token` and `session_id` from login response and set in header for all requests to authenticate.

    $ curl -X 'POST' \
        'http://localhost:8000/api/v1/receipts' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -H 'X-CSRFTOKEN: NqNxYfbdye2HKQInoFX5L8UcgJjFyZEYWDnsat6kQb47tpOvkQIU4j0iZ9nSea57' \
        -H 'X-SESSIONID: 1j743534545

## Test
For testing, moto_server need to be run in a new tab or background. For running moto_server, Flask is required and added in requirements.txt.

    $ moto_server

moto_server will be running on http://127.0.0.1:5000, then run test

    $ pytest


## Create superuser
Create superuser to test admin feature

    $ python manage.py createsuperuser
    or
    $ ./manage.py createsuperuser

# Django poll app

## Installation

To start the poll app, you need to have python 3, pip and Django installed.

For installing Python and pip you can follow e.g. [these instructions](https://realpython.com/installing-python/)

To install Django, run this command in terminal:

`python -m pip install Django`

## Running the development server

To run the development server, run the command

`python3 manage.py runserver 0.0.0.0:8000`

or when running in a container, enter commands

```
docker build -t djangopolls .
docker run -it -p 8000:8000 djangopolls
```

Polls can be found at /polls, and poll questions can be added through the admin panel from /admin. To log in as an admin, create a new admin user following instructions covered [here](https://docs.djangoproject.com/en/3.0/intro/tutorial02/)

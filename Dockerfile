FROM python:3

WORKDIR /app

RUN python -m pip install Django
COPY . /app

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000

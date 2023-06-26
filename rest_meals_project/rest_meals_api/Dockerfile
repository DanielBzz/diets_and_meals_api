FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /my_rest_meals_api
WORKDIR /my_rest_meals_api

COPY . /my_rest_meals_api/

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:5001"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:5001"]
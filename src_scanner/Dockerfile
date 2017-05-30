FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD celery-4.0.2 /code/celery-4.0.2
ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/

ENTRYPOINT ["gunicorn"]
CMD ["mysite.wsgi", "-b 0.0.0.0:8000"]

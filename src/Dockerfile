FROM ubuntu:latest
MAINTAINER Jesse Cai "jcjessecai@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

#caching pip install
RUN mkdir -p /app
RUN mkdir -p /uploads
ADD ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]
CMD ["server.py"]

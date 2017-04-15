FROM ubuntu:latest
MAINTAINER Jesse Cai "jcjessecai@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
#ugly, but necessary for textract
RUn apt-get install -y python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev

#caching pip install
RUN mkdir -p /app
ADD ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]
CMD ["server.py"]

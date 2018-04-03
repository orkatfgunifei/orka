FROM ubuntu:latest
MAINTAINER 10Adev "admin@10adev.com.br"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential postgresql python-psycopg2
RUN apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN apt-get install -y libpq-dev
RUN pip install -U pip
RUN pip install pillow

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["fabmanager", "run"]
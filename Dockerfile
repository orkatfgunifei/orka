FROM ubuntu:latest
MAINTAINER 10Adev "admin@10adev.com.br"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential postgresql python-psycopg2 gunicorn supervisor
RUN apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN apt-get install -y libpq-dev docker.io
RUN pip install -U pip
RUN pip install pillow

ADD ./entrypoint.sh /
RUN chmod 777 /entrypoint.sh

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt


# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./supervisord.conf /etc/supervisord.con
COPY ./gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

RUN chmod 777 /etc/supervisor/conf.d/supervisord.conf
RUN chmod 777 /etc/supervisord.con
RUN chmod 777 /etc/supervisor/conf.d/gunicorn.conf

ENTRYPOINT ["/entrypoint.sh"]
# Start processes
#CMD ["/usr/bin/supervisord"]
CMD ["fabmanager", "run"]
#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM ubuntu:14.04
MAINTAINER Benoît Suttor<bsuttor@imio.com>


RUN \
  apt-get update && \
  apt-get install -y build-essential && \
  apt-get install -y libxml2-dev libxslt1-dev libjpeg-dev gettext git python-dev python-pip libgdal1-dev && \
  apt-get install -y python-pillow python-lxml python-psycopg2 python-django python-bs4 python-multipartposthandler transifex-client python-paver python-nose python-django-nose python-gdal python-django-pagination python-django-jsonfield python-django-extensions python-django-taggit python-httplib2

RUN mkdir -p /opt/imio_geonode
RUN mkdir /logs

WORKDIR /opt/imio_geonode
ADD requirements.txt /opt/imio_geonode/
RUN pip install -r requirements.txt
ADD . /opt/imio_geonode/

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

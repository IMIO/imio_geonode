FROM ubuntu:14.04
MAINTAINER Benoît Suttor <bsuttor@imio.com>

RUN echo "deb http://ppa.launchpad.net/fkrull/deadsnakes-python2.7/ubuntu trusty main" > /etc/apt/sources.list.d/fkrull.list
RUN \
  apt-get update  -y && \
  apt-get install -y build-essential && \
  apt-get install -y python2.7 libxml2-dev libxslt1-dev libjpeg-dev gettext git python-dev python-pip libgdal1-dev --force-yes && \
  apt-get install -y python-pillow python-lxml python-psycopg2 python-django python-bs4 python-multipartposthandler transifex-client python-paver python-nose python-django-nose python-gdal python-django-pagination python-django-jsonfield python-django-extensions python-django-taggit python-httplib2 wget libffi-dev --force-yes

RUN mkdir -p /opt/imio_geonode
RUN mkdir /logs

WORKDIR /opt/imio_geonode
ADD requirements.txt /opt/imio_geonode/
RUN wget -qO- http://frontend1.imio.be/20150127-star.imio.be.crt >> /etc/ssl/certs/ca-certificates.crt
RUN wget -qO- http://frontend1.imio.be/20150127-star.guichet-citoyen.be.crt >> /etc/ssl/certs/ca-certificates.crt
RUN wget -qO- http://frontend1.imio.be/20150127-star.imio-app.be.crt >> /etc/ssl/certs/ca-certificates.crt

RUN pip install -U pip
RUN pip install -r requirements.txt
ADD . /opt/imio_geonode/
RUN cp -R /usr/local/geonode/*  /usr/local/lib/python2.7/dist-packages/geonode
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

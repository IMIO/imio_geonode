#!/usr/bin/make
GDALVERSION=`gdal-config --version`
LIB=['gfortran', 'libblas-dev', 'liblapack-dev']
all: run
.PHONY: install run

bin/python:
	virtualenv-2.7 --no-site-packages .

install: bin/python
	./bin/pip install -e git+git@github.com:GeoNode/geonode.git#egg=geonode
	./bin/pip install -e .
	./bin/python manage.py syncdb

run: install
	./bin/python manage.py runserver


.PHONY: cleanall
cleanall:
	rm -fr develop-eggs include parts .installed.cfg lib include bin .mr.developer.cfg
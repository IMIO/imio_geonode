#!/usr/bin/make
GDALVERSION=`gdal-config --version`

all: run
.PHONY: install run syncdb init

bin/python:
	virtualenv-2.7 .

src/imio_geonode/local_settings.py:
	cp src/imio_geonode/local_settings.py.sample src/imio_geonode/local_settings.py

install: bin/python src/imio_geonode/local_settings.py
	./bin/pip install -e git+git@github.com:GeoNode/geonode.git#egg=geonode
	./bin/pip install -e .

syncdb:
	./bin/python manage.py syncdb

init: install syncdb

run:
	./bin/python manage.py runserver 0.0.0.0:8080

update:
	git fetch upstream
	git merge upstream/IMIO

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs include parts .installed.cfg lib include bin .mr.developer.cfg *.egg-info


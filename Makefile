#!/usr/bin/make
GDALVERSION=`gdal-config --version`

all: run
.PHONY: install run syncdb init

bin/python:
	virtualenv-2.7 .

imio_geonode/local_settings.py:
	cp imio_geonode/local_settings.py.sample imio_geonode/local_settings.py

install: bin/python imio_geonode/local_settings.py
	# ./bin/pip install -e git+git@github.com:GeoNode/geonode.git#egg=geonode
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


postgres_data:
	mkdir postgres_data

geoserver_data:
	mkdir geoserver_data

docker-up: imio_geonode/local_settings.py postgres_data geoserver_data
	docker-compose up

docker-init: imio_geonode/local_settings.py
	docker-compose start
	docker exec -ti imiogeonode_geonode_1 python manage.py syncdb
	docker-compose stop

docker-image:
	docker build -t imio-geonode:latest .

docker-geoserver-image:
	cd geoserver && docker build -t imio-geoserver:latest .

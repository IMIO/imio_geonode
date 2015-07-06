#!/usr/bin/make
GDALVERSION=`gdal-config --version`

all: init
.PHONY: install run syncdb init

imio_geonode/local_settings.py:
	cp imio_geonode/local_settings.py.sample imio_geonode/local_settings.py

syncdb:
	docker-compose run --rm --entrypoint='/usr/bin/python' geonode manage.py syncdb

update:
	git fetch upstream
	git merge upstream/IMIO

.PHONY: cleanall
cleanall:
	docker-compose stop
	docker-compose rm -f

docker-update-images: cleanall
	docker-compose build

postgres_data:
	mkdir postgres_data

geoserver_data:
	mkdir geoserver_data

up: docker-up

docker-up: imio_geonode/local_settings.py postgres_data geoserver_data
	docker-compose up

init: docker-init

docker-init: imio_geonode/local_settings.py postgres_data geoserver_data
	docker-compose up postgis &
	sleep 15
	docker-compose run --rm --entrypoint='/usr/bin/python' geonode manage.py syncdb
	docker-compose stop

docker-geonode-image:
	docker build -t imio-geonode:latest .

docker-geoserver-image:
	cd Dockerfiles/geoserver && docker build -t imio-geoserver:latest .


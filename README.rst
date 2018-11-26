Imio_Geonode
============

This module extends Geonode and add some features for IMIO.

Installation
------------

* Install Docker >= 1.9 (https://docs.docker.com/installation/)

* Install docker-compose >= 1.5 (https://docs.docker.com/compose/install/)

And then, run ::

    $ docker-compose build

    $ make init

    $ docker-compose up

Now you can open your browser on http://localhost:8080

`make init` will build docker images and start Django syncdb. It also create Docker network named as docker-compose project name (name of folder by default, so imiogeonode).

You can create Docker network with `docker network create imiogeonode` command


Postgis
-------

A postgis image is created from postgres:9.4 docker image (https://registry.hub.docker.com/_/postgres/).
If you add .dump postgres files in Dockerfiles/postgis/ folder, these files will be imported into DB during first start.



This project was created with a template ::

    $ django-admin startproject imio_geonode --template=https://github.com/GeoNode/geonode-project/archive/master.zip -epy,rst


Utilitaire
----------

[out:json];area[name="België - Belgique - Belgien"];(rel[name="Mons"][admin_level=8][boundary=administrative](area););out geom;

python manage.py addurb -c admin -p admin -u docker.for.mac.localhost  -m 5432 -g postgres -d test_cadastre -a soignies -z soignies.be -n soignies-ro -r grog

Charger la configuration de reperage par defaut
-------------------------

python manage.py loaddata imio_survey.json

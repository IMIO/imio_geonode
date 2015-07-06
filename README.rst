Imio_Geonode
============

This module extends Geonode and add some feature for IMIO.

Installation
------------

* Install Docker (https://docs.docker.com/installation/)

* Install docker-compose (https://docs.docker.com/compose/install/)

And then, run ::

    $ docker-compose build

    $ make init

    $ docker-compose up

Now you can open your browser on http://localhost

`make init` will build docker images and start Django syncdb.


Postgis
-------

A postgis image is created from postgres:9.4 docker image (https://registry.hub.docker.com/_/postgres/).
If you add .dump postgres files in Dockerfiles/postgis/ folder, these files will be imported into DB during first start.



This project was created with a template ::

    $ django-admin startproject imio_geonode --template=https://github.com/GeoNode/geonode-project/archive/master.zip -epy,rst
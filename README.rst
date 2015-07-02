Imio_Geonode
============

This module extends Geonode and add some feature for IMIO.

Installation
------------

* Install Docker (https://docs.docker.com/installation/)

* Install docker-compose (https://docs.docker.com/compose/install/)

And then, run ::

    $ make init

    $ docker-compose up

Now you can open your browser on http://localhost

`make init` will build docker images and start Django syncdb.



This template was created with ::

    $ django-admin startproject imio_geonode --template=https://github.com/GeoNode/geonode-project/archive/master.zip -epy,rst
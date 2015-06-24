#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM ubuntu:trusty
MAINTAINER Benoît Suttor<bsuttor@imio.com>

RUN export DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND noninteractive
RUN dpkg-divert --local --rename --add /sbin/initctl
#RUN ln -s /bin/true /sbin/initctl
RUN apt-get install -y software-properties-common

#-------------Application Specific Stuff ----------------------------------------------------
RUN apt-get update -y
RUN apt-get install -y python python-dev python-lxml
RUN apt-get install -y gdal-bin
#RUN add-apt-repository ppa:geonode/testing
RUN add-apt-repository ppa:geonode/release
RUN apt-get update -y
RUN apt-get install -y geonode
RUN geonode-updateip 127.0.0.1
WORKDIR /opt
RUN git clone https://github.com/IMIO/imio_geonode.git /opt/imio_geonode

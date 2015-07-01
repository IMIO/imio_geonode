FROM tomcat:8-jre7
MAINTAINER Benoît Suttor <bsuttor@imio.com>


RUN apt-get update && apt-get install wget unzip

RUN wget -O /usr/local/tomcat/webapps/geoserver.war http://build.geonode.org/geoserver/latest/geoserver.war

ENV GEOSERVER_DATA_DIR /opt/geoserver/data_dir
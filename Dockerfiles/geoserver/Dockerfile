FROM tomcat:8-jre7
MAINTAINER Benoît Suttor <bsuttor@imio.com>

RUN apt-get -y update

RUN apt-get -y install wget unzip

RUN wget -O /usr/local/tomcat/webapps/geoserver.war http://build.geonode.org/geoserver/latest/geoserver.war
RUN apt-get remove -y wget

RUN openssl s_client -connect geonode.imio.be:443 2>&1 |sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > star.imio.be.crt && yes yes | keytool -import -alias ca -file star.imio.be.crt -keystore /etc/ssl/certs/java/cacerts -storepass changeit

ENV GEOSERVER_DATA_DIR /opt/geoserver/data_dir

ADD geoserver.xml /usr/local/tomcat/conf/Catalina/localhost/geoserver.xml

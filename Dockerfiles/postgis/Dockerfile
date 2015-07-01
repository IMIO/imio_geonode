FROM postgres:9.4
MAINTAINER Benoît Suttor <bsuttor@imio.com>

ENV POSTGIS_MAJOR 2.1

RUN apt-get update && apt-get install -y postgresql-9.4-postgis-2.1

# RUN ./docker-entrypoint.sh postgres
# USER postgres

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/initdb-postgis.sh

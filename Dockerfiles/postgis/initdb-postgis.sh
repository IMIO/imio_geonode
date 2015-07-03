#!/bin/sh
POSTGRES="gosu postgres"

$POSTGRES postgres --single -E <<EOSQL
CREATE ROLE geonode ENCRYPTED PASSWORD 'geonode' LOGIN;
EOSQL
$POSTGRES postgres --single -E <<EOSQL
CREATE DATABASE geonode OWNER geonode ;
CREATE DATABASE "geonode-imports" OWNER geonode ;
EOSQL
$POSTGRES pg_ctl -w start
$POSTGRES psql -d geonode-imports -c 'CREATE EXTENSION postgis;'
$POSTGRES psql -d geonode-imports -c 'GRANT ALL ON geometry_columns TO PUBLIC;'
$POSTGRES psql -d geonode-imports -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'
if [ -d /docker-entrypoint-initdb.d ]; then
    for f in /docker-entrypoint-initdb.d/*.dump; do
        [ -f "$f" ] && $POSTGRES psql -d geonode-imports -f "$f"
    done
fi
$POSTGRES pg_ctl stop
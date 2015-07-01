#!/bin/sh
POSTGRES="gosu postgres"

$POSTGRES postgres --single -E <<EOSQL
CREATE ROLE geonode ENCRYPTED PASSWORD 'geonode' LOGIN;
EOSQL
$POSTGRES postgres --single -E <<EOSQL
CREATE DATABASE geonode OWNER geonode ;
CREATE DATABASE geonode_data OWNER geonode ;
EOSQL
$POSTGRES pg_ctl -w start
$POSTGRES psql -h localhost -p 5432 -d geonode_data -c 'CREATE EXTENSION postgis;'
$POSTGRES psql -h localhost -p 5432 -d geonode_data -c 'GRANT ALL ON geometry_columns TO PUBLIC;'
$POSTGRES psql -h localhost -p 5432 -d geonode_data -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'
$POSTGRES pg_ctl stop
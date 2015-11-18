#!/bin/sh
POSTGRES="gosu postgres"

$POSTGRES psql -c "CREATE ROLE geonode ENCRYPTED PASSWORD 'geonode' LOGIN;"
$POSTGRES psql -c 'ALTER USER geonode SUPERUSER;'

$POSTGRES psql -c "CREATE DATABASE geonode OWNER geonode ;"
$POSTGRES psql -c "CREATE DATABASE test_geonode OWNER geonode ;"
$POSTGRES psql -c 'CREATE DATABASE "geonode-imports" OWNER geonode ;'
$POSTGRES psql -c 'CREATE DATABASE "test_geonode-imports" OWNER geonode ;'

$POSTGRES psql -c 'CREATE DATABASE "testdata" OWNER geonode ;'

$POSTGRES psql -d test_geonode-imports -c 'CREATE EXTENSION postgis;'
$POSTGRES psql -d test_geonode-imports -c 'GRANT ALL ON geometry_columns TO PUBLIC;'
$POSTGRES psql -d test_geonode-imports -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'

$POSTGRES psql -d geonode-imports -c 'CREATE EXTENSION postgis;'
$POSTGRES psql -d geonode-imports -c 'GRANT ALL ON geometry_columns TO PUBLIC;'
$POSTGRES psql -d geonode-imports -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'

$POSTGRES psql -d testdata -c 'CREATE EXTENSION postgis;'
$POSTGRES psql -d testdata -c 'GRANT ALL ON geometry_columns TO PUBLIC;'
$POSTGRES psql -d testdata -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'

$POSTGRES psql -d geonode < /docker-entrypoint-initdb.d/geonode_authorize_layer.sql

if [ -d /docker-entrypoint-initdb.d ]; then
    for f in /docker-entrypoint-initdb.d/*.dump; do
        [ -f "$f" ] && $POSTGRES psql -d geonode-imports -f "$f"
    done
fi

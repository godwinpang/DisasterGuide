#!/usr/bin/env bash

export PGPASSWORD=postgres
psql -h localhost -p 5432 -U postgres -d disasterguide -c 'DROP TABLE users CASCADE'
psql -h localhost -p 5432 -U postgres -d disasterguide -c 'DROP TABLE locations CASCADE'
psql -h localhost -p 5432 -U postgres -d disasterguide -c 'DROP TABLE help_log CASCADE'
psql -h localhost -p 5432 -U postgres -d disasterguide -c 'DROP TABLE distress_log CASCADE'
psql -h localhost -p 5432 -U postgres -d disasterguide -f ./DisasterGuide-server/database_schema.sql

# test /adduser
echo -n "/adduser (1): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_adduser_1.json" http://localhost:8088/adduser
echo

echo -n "/adduser (2): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_adduser_2.json" http://localhost:8088/adduser
echo

# test /getuser
echo -n "/getuser: "
curl -d "@./DisasterGuide-server/test_jsons/test_post_getuser.json" http://localhost:8088/getuser
echo

# test /addlocation
echo -n "/addlocation (1): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_addlocation_1.json" http://localhost:8088/addlocation
echo

echo -n "/addlocation (2): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_addlocation_2.json" http://localhost:8088/addlocation
echo

echo -n "/addlocation (3): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_addlocation_3.json" http://localhost:8088/addlocation
echo

# test /getlocation
echo -n "/getlocation: "
curl -d "@./DisasterGuide-server/test_jsons/test_post_getlocation.json" http://localhost:8088/getlocation
echo

# test /getlocationhistory
echo -n "/getlocationhistory: "
curl -d "@./DisasterGuide-server/test_jsons/test_post_getlocationhistory.json" http://localhost:8088/getlocationhistory
echo

# test /getallusers
echo -n "/getallusers: "
curl -X GET http://localhost:8088/getallusers
echo
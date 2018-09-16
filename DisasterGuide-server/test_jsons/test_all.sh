#!/usr/bin/env bash

export PGPASSWORD=postgres
psql -h localhost -p 5432 -U postgres -d disasterguide -c 'DROP TABLE users CASCADE'
psql -h localhost -p 5432 -U postgres -d disasterguide -c 'DROP TABLE locations CASCADE'
psql -h localhost -p 5432 -U postgres -d disasterguide -c 'DROP TABLE help_log CASCADE'
psql -h localhost -p 5432 -U postgres -d disasterguide -c 'DROP TABLE distress_log CASCADE'
psql -h localhost -p 5432 -U postgres -d disasterguide -f ./DisasterGuide-server/database_schema.sql

# test /adduser
echo -n "/adduser (1): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_adduser_1.json" http://localhost:8088/adduser | jq '.'
echo

echo -n "/adduser (2): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_adduser_2.json" http://localhost:8088/adduser | jq '.'
echo

# test /getuser
echo -n "/getuser: "
curl -d "@./DisasterGuide-server/test_jsons/test_post_getuser.json" http://localhost:8088/getuser | jq '.'
echo

# test /addlocation
echo -n "/addlocation (1): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_addlocation_1.json" http://localhost:8088/addlocation | jq '.'
echo

echo -n "/addlocation (2): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_addlocation_2.json" http://localhost:8088/addlocation | jq '.'
echo

echo -n "/addlocation (3): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_addlocation_3.json" http://localhost:8088/addlocation | jq '.'
echo

# test /getlocation
echo -n "/getlocation: "
curl -d "@./DisasterGuide-server/test_jsons/test_post_getlocation.json" http://localhost:8088/getlocation | jq '.'
echo

# test /getlocationhistory
echo -n "/getlocationhistory: "
curl -d "@./DisasterGuide-server/test_jsons/test_post_getlocationhistory.json" http://localhost:8088/getlocationhistory | jq '.'
echo

# test /getallusers
echo -n "/getallusers: "
curl -X GET http://localhost:8088/getallusers | jq '.'
echo

# test /help
echo -n "/help (1): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_help_1.json" http://localhost:8088/help | jq '.'
echo

echo -n "/help (2): "
curl -d "@./DisasterGuide-server/test_jsons/test_post_help_2.json" http://localhost:8088/help | jq '.'
echo

# test /getwatsoncontext
echo -n "/getwatsoncontext: "
curl -d "@./DisasterGuide-server/test_jsons/test_post_getwatsoncontext.json" http://localhost:8088/getwatsoncontext | jq '.'
echo
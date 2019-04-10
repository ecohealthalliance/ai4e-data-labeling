#!/bin/bash

# I tried to 
terms=$(sed 's/.*/"&"/' terms | paste -sd ',' -)
terms="[$terms]"
query="{ \"text_matches\": { \"\$in\": $terms } }\""
echo $query

mongodump -d pmc -c articles -q '{ "text_matches": { "$in": ["field work","fieldwork","field study","field site","field area","study site","study location","study area","research site","research location","research area","sampling site","sampling location","sampling area"] } }' --archive "dump.zip"
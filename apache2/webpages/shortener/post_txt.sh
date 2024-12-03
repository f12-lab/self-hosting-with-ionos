#!/bin/bash

source .env

# Obtiene los parámetros
short_hash=$1
long_url=$2

# Realiza la petición para registrar el TXT record
curl --http1.1 -X "POST" \
    "https://api.hosting.ionos.com/dns/v1/zones/$zoneId/records" \
    -H "accept: application/json" \
    -H "X-API-Key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "[
         {
             \"name\": \"${short_hash}.shortener.fondomarcador.com\",
             \"type\": \"TXT\",
             \"content\": \"${long_url}\",
             \"ttl\": 3600,
             \"prio\": 0,
             \"disabled\": false
         }
     ]"

#!/bin/bash

# Load the file variables .env
source .env

# Make the request with curl
curl -X 'POST' \
  'https://api.hosting.ionos.com/dns/v1/dyndns' \
  -H 'accept: application/json' \
  -H "X-API-Key: $API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
  "domains": [
    "fondomarcador.com",
    "www.fondomarcador.com",
    "grafana.fondomarcador.com"
  ],
  "description": "My DynamicDns"
}'
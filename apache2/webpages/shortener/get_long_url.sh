#!/bin/bash

source .env

url="https://dns.google/resolve?name=$short_hash.shortener.fondomarcador.com&type=TXT"

response=$(curl -s "$url")

last_data=$(echo "$response" | jq -r '.Answer | select(. != null) | .[-1].data')

if [ -z "$last_data" ]; then
  echo "No se encontraron registros TXT para $short_hash.shortener.fondomarcador"
else
  echo "${last_data//\"/}"
fi
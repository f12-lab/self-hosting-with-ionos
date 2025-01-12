#!/bin/bash
set -e

# Iniciar PHP-FPM en segundo plano
php-fpm8.2 -F &

# Iniciar Nginx en modo daemon off
nginx -g "daemon off;"

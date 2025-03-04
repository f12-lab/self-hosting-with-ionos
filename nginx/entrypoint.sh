#!/bin/bash
set -e  # Detiene el script si hay errores

# Iniciar PHP-FPM en segundo plano
php-fpm8.2 -F &

# Iniciar Nginx en modo foreground
nginx -g "daemon off;"
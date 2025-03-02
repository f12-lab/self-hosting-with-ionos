#!/bin/bash
set -e  # Detiene el script si hay errores

# Iniciar Icecast en segundo plano
service icecast2 start

# Iniciar PHP-FPM en segundo plano
php-fpm8.2 -F &

# Activar el entorno virtual de Python
source /usr/local/bin/telegram/myenv/bin/activate

# Iniciar el bot de Telegram y el backend en segundo plano
python /usr/local/bin/telegram/bot.py &
python /usr/local/bin/telegram/backend.py &
python /usr/local/bin/telegram/icecast.py &

# Iniciar Nginx en modo foreground
nginx -g "daemon off;"
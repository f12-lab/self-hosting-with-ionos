#!/bin/bash
set -e  # Detiene el script si hay errores

# Iniciar PHP-FPM en segundo plano
php-fpm8.2 -F &

# Activar el entorno virtual de Python
source /usr/local/bin/telegram/myenv/bin/activate

# Iniciar el bot de Telegram y el backend en segundo plano
python /usr/local/bin/telegram/bot.py &
python /usr/local/bin/telegram/backend.py &

# Iniciar Nginx en modo foreground
nginx -g "daemon off;"
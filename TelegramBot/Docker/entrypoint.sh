#!/bin/bash
# Activar el entorno virtual de Python
source /usr/local/bin/telegram/myenv/bin/activate

# Iniciar el bot de Telegram y el backend en segundo plano
python /usr/local/bin/telegram/bot.py &
python /usr/local/bin/telegram/backend.py &
python /usr/local/bin/telegram/icecast.py &

tail -f /dev/null
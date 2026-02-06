# Usamos la imagen base de Debian
FROM debian:latest

# Actualizamos los repositorios y luego instalamos Ices2 y Vorbis-tools
RUN apt-get update && \
    apt-get install -y \
        python3 python3-pip python3-venv \
        ffmpeg \
        ca-certificates \
        curl \
        && update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copiar bot de Telegram
COPY scripts/telegramBot/ /usr/local/bin/telegram

RUN mkdir /songs /videos

# Definir el directorio de trabajo
WORKDIR /usr/local/bin/telegram

# Crear el entorno virtual e instalar dependencias
RUN python3 -m venv myenv && \
    /usr/local/bin/telegram/myenv/bin/python -m ensurepip && \
    /usr/local/bin/telegram/myenv/bin/python -m pip install --no-cache-dir -U python_dotenv python-telegram-bot yt_dlp flask requests

# Copiar script de entrada
COPY scripts/telegramBot/docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
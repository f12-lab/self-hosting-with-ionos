FROM debian:bookworm-slim

# Variables de entorno
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Nginx, PHP, utilidades y otros paquetes necesarios
RUN apt-get update && \
    apt-get install -y \
    nginx \
    libnginx-mod-rtmp \
    ffmpeg \
    icecast2 \
    ices2 \
    vorbis-tools \
    python3 \
    python3-pip \
    python3-venv \
    php-fpm \
    openssl \
    curl \
    jq \
    apt-transport-https \
    wget \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Crear directorios esenciales con permisos adecuados
RUN mkdir -p /var/log/nginx /var/run/nginx /etc/nginx/ssl /var/www/webpages /usr/local/bin/telegram && \
    chown -R www-data:www-data /var/www/webpages /var/log/nginx /var/run/nginx && \
    chmod -R 755 /var/www/webpages

# Configurar certificados SSL
COPY .certs/_.fondomarcador.com_private_key.key /etc/nginx/ssl/
COPY .certs/fondomarcador.com_ssl_certificate.cer /etc/nginx/ssl/
COPY .certs/intermediate2.cer /etc/nginx/ssl/
RUN chmod 600 /etc/nginx/ssl/*.key && chmod 644 /etc/nginx/ssl/*.cer

# Copiar archivos de configuración y páginas web
COPY nginx/webpages/ /var/www/webpages/
RUN chown -R www-data:www-data /var/www/webpages && chmod -R 755 /var/www/webpages

COPY .htpasswd/.htpasswd_admin /etc/nginx/.htpasswd_admin
RUN chown www-data:www-data /etc/nginx/.htpasswd_admin && chmod 644 /etc/nginx/.htpasswd_admin

COPY .htpasswd/.htpasswd_sysadmin /etc/nginx/.htpasswd_sysadmin
RUN chown www-data:www-data /etc/nginx/.htpasswd_sysadmin && chmod 644 /etc/nginx/.htpasswd_sysadmin

COPY nginx/webpages/shortener/.env /var/www/webpages/shortener/.env
RUN chown www-data:www-data /var/www/webpages/shortener/.env && chmod 775 /var/www/webpages/shortener/.env

# Copiar archivos de configuración de Nginx
COPY nginx/nginxconf/fondomarcador.conf /etc/nginx/sites-available/fondomarcador
COPY nginx/nginxconf/nginx.conf /etc/nginx/nginx.conf

# Crear enlaces simbólicos para habilitar el sitio y servicios de Nginx
RUN ln -s /etc/nginx/sites-available/fondomarcador /etc/nginx/sites-enabled/

# Configurar PHP-FPM (descomentando la configuración necesaria en php.ini)
RUN sed -i 's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/' /etc/php/*/fpm/php.ini

# Copiar bot de Telegram
COPY TelegramBot/ /usr/local/bin/telegram

# Asegurarse de crear el grupo y usuario correctamente
RUN useradd -r -g icecast icecast

# Copiar y configurar el archivo de configuración de Icecast
COPY icecast/icecast.xml /etc/icecast2/icecast.xml
RUN chown -R root:root /etc/icecast2 && chmod -R 755 /etc/icecast2

# Configurar directorios adicionales
RUN mkdir /etc/ices2 && chown -R root:root /etc/ices2 && chmod -R 755 /etc/ices2
COPY icecast/ices-playlist.xml /etc/ices2/ices-playlist.xml

# Configurar directorios para la música y archivos
RUN mkdir /home/musica
COPY icecast/lista.txt /home/musica/lista.txt
COPY icecast/mymusic/Prueba.ogg /home/musica/Prueba.ogg
RUN chown -R root:root /home/musica && chmod -R 755 /home/musica

# Configurar directorios para los logs
RUN mkdir -p /var/log/ices && chown -R root:root /var/log/ices && chmod -R 755 /var/log/ices
RUN touch /var/log/ices/ices.log && chown root:root /var/log/ices/ices.log && chmod 644 /var/log/ices/ices.log

# Definir el directorio de trabajo
WORKDIR /usr/local/bin/telegram

# Crear el entorno virtual e instalar dependencias
RUN python3 -m venv myenv && \
    /usr/local/bin/telegram/myenv/bin/python -m ensurepip && \
    /usr/local/bin/telegram/myenv/bin/python -m pip install --no-cache-dir python_dotenv python-telegram-bot yt_dlp flask requests

# Copiar script de entrada
COPY nginx/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Exponer puertos para HTTP, HTTPS y el bot Flask
EXPOSE 80 443 1935 5000 5001 8000

# Ejecutar el entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

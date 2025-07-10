FROM debian:bookworm-slim

# Variables de entorno
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Nginx, PHP, utilidades y otros paquetes necesarios
RUN apt-get update && \
    apt-get install -y \
    nginx \
    libnginx-mod-rtmp \
    ffmpeg \
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
COPY src/nginx/webpages/ /var/www/webpages/
RUN chown -R www-data:www-data /var/www/webpages && chmod -R 755 /var/www/webpages

COPY .htpasswd/.htpasswd_admin /etc/nginx/.htpasswd_admin
RUN chown www-data:www-data /etc/nginx/.htpasswd_admin && chmod 644 /etc/nginx/.htpasswd_admin

COPY .htpasswd/.htpasswd_sysadmin /etc/nginx/.htpasswd_sysadmin
RUN chown www-data:www-data /etc/nginx/.htpasswd_sysadmin && chmod 644 /etc/nginx/.htpasswd_sysadmin

COPY .htpasswd/.htpasswd_dante /etc/nginx/.htpasswd_dante
RUN chown www-data:www-data /etc/nginx/.htpasswd_dante && chmod 644 /etc/nginx/.htpasswd_dante

COPY src/nginx/webpages/shortener/.env /var/www/webpages/shortener/.env
RUN chown www-data:www-data /var/www/webpages/shortener/.env && chmod 775 /var/www/webpages/shortener/.env

# Copiar archivos de configuración de Nginx
COPY src/nginx/nginxconf/fondomarcador.conf /etc/nginx/sites-available/fondomarcador
COPY src/nginx/nginxconf/nginx.conf /etc/nginx/nginx.conf

# Crear enlaces simbólicos para habilitar el sitio y servicios de Nginx
RUN ln -s /etc/nginx/sites-available/fondomarcador /etc/nginx/sites-enabled/

# Configurar PHP-FPM (descomentando la configuración necesaria en php.ini)
RUN sed -i 's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/' /etc/php/*/fpm/php.ini

# Copiar script de entrada
COPY src/nginx/docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Exponer puertos para HTTP, HTTPS y el bot Flask
EXPOSE 80 443 1935

# Ejecutar el entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

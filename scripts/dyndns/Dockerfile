# Imagen base ligera
FROM debian:bookworm-slim

# Configuración de entorno
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias y cron
RUN apt-get update && apt-get install -y \
    cron \
    wget \
    jq \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configuración del script de DynDNS
WORKDIR /opt/dyndns

COPY DynDNS.sh /opt/dyndns/
COPY DDNS-cronjob /opt/dyndns/
COPY .env /opt/dyndns/

# Copiar y configurar el cronjob
COPY DDNS-cronjob /etc/cron.d/DDNS-cronjob

# Establecer permisos necesarios
RUN chmod +x /opt/dyndns/DynDNS.sh && \
    chmod 0644 /etc/cron.d/DDNS-cronjob && \
    crontab /etc/cron.d/DDNS-cronjob

# Comando para iniciar cron y mantener el contenedor activo
CMD ["cron", "-f"]
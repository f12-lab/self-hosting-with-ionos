FROM debian:bookworm

# Instalar paquetes necesarios
RUN apt-get update && apt-get install -y \
    curl \
    php \
    libapache2-mod-php \
    gnupg \
    jq \
    gnupg2 \
    supervisor \
    software-properties-common \
    apt-transport-https \
    wget && rm -rf /var/lib/apt/lists/*

# Crear directorio para llaves de APT
RUN mkdir -p /etc/apt/keyrings && chmod 0755 /etc/apt/keyrings

# Añadir llave GPG de Grafana y repositorio
RUN wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor > /etc/apt/keyrings/grafana.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" \
    > /etc/apt/sources.list.d/grafana.list

# Instalar Grafana y Prometheus
RUN apt-get update && apt-get install -y \
    grafana \
    prometheus && rm -rf /var/lib/apt/lists/*

# Copiar configuración de Grafana y Prometheus
COPY grafana.ini /etc/grafana/grafana.ini
COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY apache_exporter.service /etc/systemd/system/apache_exporter.service
COPY datasources.yml /etc/grafana/provisioning/datasources/datasources.yml
COPY dashboard.json /var/lib/grafana/dashboards/dashboard.json
COPY dashboard.yml /etc/grafana/provisioning/dashboards/dashboard.yml

# Configurar directorios y permisos
RUN mkdir -p /var/lib/grafana/dashboards /etc/grafana/provisioning/dashboards \
    && chown -R grafana:grafana /var/lib/grafana/dashboards /etc/grafana/provisioning/dashboards \
    && chmod -R 0755 /var/lib/grafana/dashboards /etc/grafana/provisioning/dashboards \
    && chmod 0644 /etc/grafana/provisioning/datasources/datasources.yml

# Descargar y configurar Apache Exporter
RUN curl -s https://api.github.com/repos/Lusitaniae/apache_exporter/releases/latest \
    | grep browser_download_url | grep linux-amd64 | cut -d '"' -f 4 | wget -qi - \
    && tar xvf apache_exporter-*.linux-amd64.tar.gz -C /tmp \
    && mv /tmp/apache_exporter-*/apache_exporter /usr/local/bin/apache_exporter \
    && chmod 0755 /usr/local/bin/apache_exporter && rm -rf /tmp/apache_exporter-*

# Recargar configuración del sistema y servicios
RUN mkdir -p /etc/supervisor/conf.d
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Exponer puertos necesarios
EXPOSE 3000 9090

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf", "-n"]
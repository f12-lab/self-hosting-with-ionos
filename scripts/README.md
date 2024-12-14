# Scripts Directory Documentation

The `scripts` directory contains automation and configuration scripts divided into two primary sections: **Dynamic DNS** and **Monitoring**. These scripts streamline domain management and enable server performance tracking through Grafana, Prometheus, and Apache Exporter.

### Directory Structure
```plaintext
scripts/
├── DynDNS.sh
├── DDNS-cronjob
├── README.md
└── grafana/
    ├── apache_exporter.service
    ├── dashboard.yml
    ├── datasources.yml
    ├── grafana.ini
    └── prometheus.yml
```

---

## Dynamic DNS

The dynamic DNS setup ensures that the IP addresses for the domain `fondomarcador.com` and its subdomains are always up-to-date.

### Script: `DynDNS.sh`
This script sends a request to the IONOS API to update the DNS records dynamically. While the script can be executed manually for testing, it is primarily automated using the `DDNS-cronjob` file.

#### Testing the Script
1. Ensure the `.env` file contains the API key:
   ```bash
   API_KEY=<your_api_key>
   ```
2. Execute the script manually to verify functionality:
   ```bash
   bash DynDNS.sh
   ```

#### Code Explanation
The `DynDNS.sh` script:
- Loads environment variables, including the `API_KEY` from `.env`.
- Makes a POST request to the IONOS API to update DNS records for `fondomarcador.com` and related subdomains.

Key section:
```bash
curl -X 'POST' \
  'https://api.hosting.ionos.com/dns/v1/dyndns' \
  -H 'accept: application/json' \
  -H "X-API-Key: $API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
  "domains": [
    "fondomarcador.com",
    "www.fondomarcador.com",
    "grafana.fondomarcador.com"
  ],
  "description": "My DynamicDns"
}'
```
This ensures that DNS records for specified domains are updated to reflect the current IP.

### Automating Updates with Cron
To automate DNS updates, the cron job runs every 5 minutes using the `DDNS-cronjob` file:

**`DDNS-cronjob`**
```plaintext
*/5 * * * * /home/vagrant/scripts/DynDNS.sh
```
This cron job ensures the dynamic DNS records stay updated without manual intervention.

---

## Monitoring

This section configures monitoring tools to track server health and activity. Key components include **Grafana**, **Prometheus**, and **Apache Exporter**. The configuration process is defined in `monitoring.yml`, making it easy to provision the required services.

### Apache Exporter
Apache Exporter collects metrics from the Apache server via the `/server-status` endpoint.

#### Service File: `apache_exporter.service`
The Apache Exporter runs as a service to continuously scrape Apache metrics. Key parameters include:
- `--scrape_uri=http://localhost/server-status/?auto`: Specifies the endpoint for scraping metrics.
- `--telemetry.endpoint=/metrics`: Defines the telemetry endpoint for Prometheus.

```ini
[Unit]
Description=Prometheus Apache Exporter
Documentation=https://github.com/Lusitaniae/apache_exporter
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=prometheus
Group=prometheus
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/usr/local/bin/apache_exporter \
  --insecure \
  --scrape_uri=http://localhost/server-status/?auto \
  --telemetry.endpoint=/metrics

SyslogIdentifier=apache_exporter
Restart=always

[Install]
WantedBy=multi-user.target
```

### Prometheus
Prometheus gathers metrics from various exporters and feeds this data to Grafana for visualization.

#### Configuration File: `prometheus.yml`
The `prometheus.yml` file includes:
- `scrape_interval: 15s`: Prometheus scrapes targets every 15 seconds.
- Targets like `localhost:9117` (Apache Exporter).

```yaml
scrape_configs:
  - job_name: "apache1"
    static_configs:
      - targets: ["localhost:9117"]
        labels:
          alias: fondo-apache-server
```

### Grafana
Grafana visualizes server metrics in a user-friendly dashboard.

#### Configuration Files:

1. **`grafana.ini`**
   Configures server settings and enables anonymous access:
   ```ini
   [server]
   domain = grafana.fondomarcador.com
   root_url = %(protocol)s://%(domain)s/

   [auth.anonymous]
   enabled = true
   org_name = Main Org.
   org_role = Viewer
   ```

2. **`datasources.yml`**
   Sets up Prometheus as the default datasource:
   ```yaml
   datasources:
     - name: Prometheus
       type: prometheus
       access: proxy
       url: http://localhost:9090
       isDefault: true
       jsonData:
         timeInterval: "10s"
   ```

3. **`dashboard.yml`**
   Automatically loads dashboards into Grafana:
   ```yaml
   providers:
     - name: "fondomarcador-dashboard"
       orgId: 1
       folder: ""
       type: file
       options:
         path: /var/lib/grafana/dashboards
   ```

#### Grafana Dashboard
A preconfigured dashboard offers visual insights into server activity and health. Key metrics include:
- Requests per second.
- Response times.
- Server uptime.

> ![Grafana Dashboard](path-to-dashboard-screenshot.png)

---

## Conclusion

The scripts in this directory enable seamless dynamic DNS updates and comprehensive server monitoring through well-integrated tools. For detailed provisioning, refer to the [monitoring.yml](../ansible/tasks/monitoring.yml) file, which automates setup for Prometheus, Grafana, and Apache Exporter. Together, these tools ensure a reliable and scalable infrastructure for `fondomarcador.com`. The Grafana dashboard provides real-time metrics to visualize the health and performance of your server infrastructure.
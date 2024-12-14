# Ansible Directory Documentation

The `ansible` directory is designed for automated provisioning and configuration of the server. It includes the inventory file, playbook, and tasks necessary to set up and manage the `fondomarcador.com` infrastructure.

---

## Structure

```plaintext
ansible/
├── hosts
├── sites.yml
└── tasks/
    ├── apache.yml
    ├── dynamic_ip.yml
    ├── monitoring.yml
    ├── ssl.yml
    └── webpages.yml
```

---

## Overview

### `hosts`
An inventory file defining the target server:

[More Details](./hosts)

---

### `sites.yml`
This is the primary playbook that orchestrates the server provisioning process. It includes:
- **Apache Configuration** (`apache.yml`)
- **SSL Setup** (`ssl.yml`)
- **Webpages Deployment** (`webpages.yml`)
- **Dynamic DNS Updates** (`dynamic_ip.yml`)
- **Monitoring Tools** (`monitoring.yml`)

[More Details](./sites.yml)

---

## Tasks

### `apache.yml`
Automates Apache installation and configuration:
- Updates the package list.
- Installs Apache and utilities.
- Deploys custom configurations like `fondomarcador.conf`.

[More Details](./tasks/apache.yml)

---

### `dynamic_ip.yml`
Manages the scripts required for Dynamic DNS updates:
- Copies the `DynDNS.sh` script to the server.
- Sets up a cron job (`DDNS-cronjob`) to execute the script every 5 minutes.

[More Details](./tasks/dynamic_ip.yml)

---

### `monitoring.yml`
Handles the installation and setup of Grafana, Prometheus, and Apache Exporter:
- Installs Grafana and Prometheus.
- Configures dashboards and datasources for Grafana.
- Sets up Apache Exporter for Apache metrics.

[More Details](./tasks/monitoring.yml)

---

### `ssl.yml`
Ensures the secure deployment of SSL certificates:
- Creates a directory for certificates.
- Deploys `.key` and `.crt` files for HTTPS connections.

[More Details](./tasks/ssl.yml)

---

### `webpages.yml`
Deploys the website files and sets appropriate permissions:
- Synchronizes the `webpages` directory to the server.
- Configures authentication files for protected areas like `/admin`.
- Ensures correct ownership and permissions.

[More Details](./tasks/webpages.yml)

---

## Usage

1. Define the target server in `hosts`.
2. Update the `sites.yml` playbook with the desired task files.
3. Run the playbook:
   ```bash
   ansible-playbook -i hosts sites.yml
   ```

---

## Conclusion

This directory provides a modular and streamlined approach to managing `fondomarcador.com`'s server. Each task file focuses on a specific function, from Apache setup to advanced monitoring with Grafana. By leveraging Ansible, the entire setup is automated, repeatable, and scalable.
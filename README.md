# Self hosting with IONOS

Welcome to the **Fondomarcador.com**! This repository contains the infrastructure and configurations for setting up a web server and its associated tools. The primary goal of this project is to deploy a robust and functional environment with features like dynamic DNS, SSL certificates, monitoring, and a URL shortener application, using vagrant and ansible.

## Features

- **Dynamic DNS**: Automates the process of updating DNS records with current IP addresses.
- **SSL Certificates**: Secure your domain with SSL certificates.
- **Monitoring**: Preconfigured Grafana dashboards for server status and performance.
- **URL Shortener**: A simple yet powerful URL shortener application.
- **Custom Error Pages**: Includes tailored 401 and 404 error pages.
- **Apache Web Server**: Configured to host multiple sites with SSL support.

---

## Repository Structure

Here’s an overview of the repository structure:

```plaintext
├── ansible
│   ├── hosts
│   ├── sites.yml
│   └── tasks
│       ├── apache.yml
│       ├── dynamic_ip.yml
│       ├── monitoring.yml
│       ├── ssl.yml
│       └── webpages.yml
├── apache2
│   ├── apache2.conf
│   ├── fondomarcador.conf
│   └── webpages
│       ├── index.html
│       ├── logo.png
│       ├── README.md
│       ├── admin
│       │   ├── admin.html
│       │   └── image.png
│       ├── CSS
│       │   ├── admin.css
│       │   ├── errors.css
│       │   ├── index.css
│       │   └── shortener.css
│       ├── errors
│       │   ├── 401.html
│       │   └── 404.php
│       └── shortener
│           ├── get_long_url.sh
│           ├── get_url.sh
│           ├── index.php
│           └── post_txt.sh
├── scripts
│   ├── DDNS-cronjob
│   ├── DynDNS.sh
│   └── grafana
│       ├── apache_exporter.service
│       ├── dashboard.json
│       ├── dashboard.yml
│       ├── datasources.yml
│       ├── grafana.ini
│       └── prometheus.yml
```

> Each folder will contain a specific `README.md` file for detailed explanations. Navigate to the folder and open the respective README for more details.

---

## Getting Started

Follow these steps to set up the environment on your machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/f12-lab/self-hosting-with-ionos
   cd self-hosting-with-ionos
   ```

2. Install the required tools:
   - Vagrant
   - Ansible
   - VirtualBox

3. Start the Vagrant environment:
   ```bash
   vagrant up
   ```

4. Access the web server via the IP or domain configured.

---

## Folder Details

### ansible
Includes Ansible playbooks for provisioning the server.

[More Details](./ansible/)

### apache2
Holds Apache configuration files, hosted webpages, details of the URL shortener functionality, and server performance test results.

[More Details](./apache2/)

### scripts
Automation scripts for dynamic DNS, monitoring, and more. Includes preconfigured Grafana settings:
- **Dashboards**: Visualize Apache metrics like requests per second, server status, and response times.
- **Prometheus Integration**: Collects and stores metrics for efficient monitoring.
- **Exporters**: Configured `apache_exporter` to gather data directly from the web server.

[More Details](./scripts/)

---

## Opening Ports

Inside your router, you need to open ports 80 (HTTP) and 443 (HTTPS) to ensure proper server access and SSL configuration.

![ports image in router](https://github.com/M-L56/self-hosting-with-ionos/blob/12529c1b2710c5347e13eb959e802d787af783f8/images/ports.png)

---

## Contributions

Feel free to contribute to this project. Submit a pull request or open an issue for suggestions and improvements.

---

## License

This project is licensed under the GNU GPLv3 License. See the [LICENSE](./LICENSE) file for details.

---

## Contact

For any questions, reach out at [malutrab63@gmail.com](mailto:malutrab63@gmail.com).

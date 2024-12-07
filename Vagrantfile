# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"

  config.vm.define "server" do |server|
    server.vm.network "private_network", ip: "192.168.57.10"
    server.vm.network "forwarded_port", guest: 80, host: 8080
    server.vm.network "forwarded_port", guest: 443, host: 8443
    server.vm.network "forwarded_port", guest: 3000, host: 3000
    server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      # Configure apache2 
      apt-get -y install apache2 apache2-utils
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
      cp -v /vagrant/apache2/fondomarcador.conf /etc/apache2/sites-available
      sudo a2ensite fondomarcador.conf
      # SSL
      sudo mkdir -p /etc/apache2/ssl
      sudo chmod 700 /etc/apache2/ssl

      cp -v /vagrant/.certs/_.fondomarcador.com_private_key.key /etc/apache2/ssl/private.key
      cp -v /vagrant/.certs/fondomarcador.com_ssl_certificate.cer /etc/apache2/ssl/certificate.crt
      cp -v /vagrant/.certs/intermediate2.cer /etc/apache2/ssl/intermediate.crt

      sudo chmod 600 /etc/apache2/ssl/private.key

      sudo a2enmod ssl
      sudo a2enmod rewrite

      # Web pages
      cp -vr /vagrant/apache2/webpages/ /var/www/
      ## CSS
      sudo chown -R www-data:www-data /var/www/html/CSS
      ## Index
      ## Errors
      sudo chown -R www-data:www-data /var/www/html/errors
      ## Image
      sudo a2enmod headers 
      ## Admin
      sudo chown -R www-data:www-data /var/www/html/admin
      ## Status (doesn't work)
      sudo chown -R www-data:www-data /var/www/html/status
      ### .htpasswd
      cp /vagrant/.htpasswd/.htpasswd_admin /etc/apache2/.htpasswd_admin
      cp /vagrant/.htpasswd/.htpasswd_sysadmin /etc/apache2/.htpasswd_sysadmin
      ## Dinamic IP
      mkdir -p /home/vagrant/scripts
      cp /vagrant/scripts/ /home/vagrant/scripts/
      chmod +x /home/vagrant/scripts/DynDNS.sh
      chmod 644 /home/vagrant/scripts/.env
      cp /vagrant/config/dynamic-dns/DDNS-cronjob /etc/cron.d/
      #Shortener
      sudo chmod 777 /var/www/webpages/shortener/.env
      # Grafana

      apt-get install -y curl php libapache2-mod-php gnupg jq
      sudo a2enmod proxy
      sudo a2enmod proxy_http
      sudo apt install -y gnupg2 software-properties-common apt-transport-https wget
      sudo mkdir -p /etc/apt/keyrings/
      wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
      echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
      sudo apt-get update -y
      sudo apt-get install grafana -y
      cp /vagrant/scripts/grafana/grafana.ini /etc/grafana/
      systemctl restart grafana-server
      systemctl restart apache2
      curl -s https://api.github.com/repos/Lusitaniae/apache_exporter/releases/latest|grep browser_download_url|grep linux-amd64|cut -d '"' -f 4|wget -qi -
      tar xvf apache_exporter-*.linux-amd64.tar.gz
      sudo cp apache_exporter-*.linux-amd64/apache_exporter /usr/local/bin
      sudo chmod +x /usr/local/bin/apache_exporter
      sudo groupadd --system prometheus
      sudo useradd -s /sbin/nologin --system -g prometheus prometheus
      cp /vagrant/scripts/grafana/apache_exporter.service /etc/systemd/system/apache_exporter.service
      sudo systemctl daemon-reload
      sudo systemctl restart apache_exporter.service
      apt install prometheus -y
      cp /vagrant/scripts/grafana/prometheus.yml /etc/prometheus/
      sudo systemctl restart prometheus
       # Crear carpetas para dashboards
      mkdir -p /var/lib/grafana/dashboards
      mkdir -p /etc/grafana/provisioning/dashboards

      # Copiar el dashboard
      cp /vagrant/scripts/grafana/dashboard.json /var/lib/grafana/dashboards/
      cp /vagrant/scripts/grafana/dashboard.yml /etc/grafana/provisioning/dashboards/

      sudo chown grafana:grafana /var/lib/grafana/dashboards/dashboard.json
      sudo chmod 644 /var/lib/grafana/dashboards/dashboard.json
      sudo systemctl restart grafana-server
      # Crear el directorio de provisión de Grafana si no existe
      sudo mkdir -p /etc/grafana/provisioning/datasources

      # Copiar el archivo de configuración YAML desde el host
      sudo cp /vagrant/scripts/grafana/datasources.yml /etc/grafana/provisioning/datasources/

      # Reiniciar Grafana para aplicar la configuración
      sudo systemctl restart grafana-server

      # Enable apache2
      systemctl restart apache2
    SHELL
  end
end
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
      #sudo apt install certbot python3-certbot-apache -y
      #sudo certbot --apache --non-interactive --agree-tos --email mquepra130@ieszaidinvergeles.org -d fondomarcador.com
      # Web pages
      ## CSS
      mkdir /var/www/html/CSS
      sudo chown -R www-data:www-data /var/www/html/CSS
      cp -v /vagrant/apache2/webpages/CSS/index.css /var/www/html/CSS
      cp -v /vagrant/apache2/webpages/CSS/admin.css /var/www/html/CSS
      cp -v /vagrant/apache2/webpages/CSS/errors.css /var/www/html/CSS
      ## Index
      cp -v /vagrant/apache2/webpages/index.html /var/www/html
      ## Errors
      mkdir /var/www/html/errors
      sudo chown -R www-data:www-data /var/www/html/errors
      cp -v /vagrant/apache2/webpages/errors/404.html /var/www/html/errors 
      #cp -v /vagrant/apache2/webpages/errors/401.html /var/www/html/errors
      ## Image
      sudo a2enmod headers 
      cp -v /vagrant/apache2/webpages/logo.png /var/www/html
      ## Admin
      mkdir /var/www/html/admin
      sudo chown -R www-data:www-data /var/www/html/admin
      cp -v /vagrant/apache2/webpages/admin/.htaccess /var/www/html/admin/
      cp -v /vagrant/apache2/webpages/admin/admin.html /var/www/html/admin/
      cp -v /vagrant/apache2/webpages/admin/image.png /var/www/html/admin/
      cp -v /vagrant/apache2/webpages/errors/401.html /var/www/html/admin/
      ### .htpasswd
      cp /vagrant/.htpasswd/.htpasswd_admin /etc/apache2/.htpasswd_admin
      cp /vagrant/.htpasswd/.htpasswd_sysadmin /etc/apache2/.htpasswd_sysadmin
      ## Dinamic IP
      mkdir -p /home/vagrant/scripts
      cp /vagrant/scripts/ /home/vagrant/scripts/
      chmod +x /home/vagrant/scripts/DynDNS.sh
      chmod 644 /home/vagrant/scripts/.env
      (crontab -l 2>/dev/null; echo "*/5 * * * * /home/vagrant/scripts/DynDNS.sh") | crontab -
      
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

      # Configurar el provisioning
      cat <<EOF > /etc/grafana/provisioning/dashboards/dashboard.yml
apiVersion: 1
providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: 'file'
    disableDeletion: false
    editable: false
    options:
      path: /var/lib/grafana/dashboards
EOF
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

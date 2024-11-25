# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"

  config.vm.define "server" do |server|
    server.vm.network "private_network", ip: "192.168.57.10"
    server.vm.network "forwarded_port", guest: 80, host: 8080
    server.vm.network "forwarded_port", guest: 443, host: 8443
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
      cp /vagrant/scripts/DynDNS.sh /home/vagrant/scripts
      chmod +x /home/vagrant/scripts/DynDNS.sh
      (crontab -l 2>/dev/null; echo "*/5 * * * * /home/vagrant/scripts/DynDNS.sh") | crontab -
      # Enable apache2
      systemctl restart apache2
    SHELL
  end
end

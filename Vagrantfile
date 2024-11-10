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
      apt-get -y install apache2
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
      cp -v /vagrant/apache2/fondomarcador.conf /etc/apache2/sites-available
      # SSL
      sudo apt install certbot python3-certbot-apache -y
      sudo certbot --apache --non-interactive --agree-tos --email mquepra130@ieszaidinvergeles.org -d fondomarcador.com
      # Web pages
      cp -v /vagrant/apache2/webpages/index.html /var/www/html
      # Dinamic IP
      mkdir -p /home/vagrant/scripts
      cp /vagrant/scripts/DynDNS.sh /home/vagrant/scripts
      chmod +x /home/vagrant/scripts/DynDNS.sh
      (crontab -l 2>/dev/null; echo "*/5 * * * * /home/vagrant/scripts/DynDNS.sh") | crontab -
      #Enable apache2
      sudo a2ensite fondomarcador.conf
      systemctl restart apache2
    SHELL
  end
end

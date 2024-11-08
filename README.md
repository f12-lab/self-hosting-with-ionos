# Self hosting with IONOS
First of all we need a domain in Ionos to perform the following practice. In this practice we will create a virtual machine that will be our server, then we will provision it with Apache2. We will then bind our domain to the ip using a python script that will start every time we start the vm.

## Opening ports
Inside our router we need to open ports 80 and 443.

![ports image in router](https://github.com/M-L56/self-hosting-with-ionos/blob/12529c1b2710c5347e13eb959e802d787af783f8/images/ports.png)

## IONOS DynDNS

We have to go to this web page [IONOS DNS](https://developer.hosting.ionos.es/docs/dns), and we have to click on Authorize, inside we enter our public and private keys that Ionos gave us before, in this way: `public.private`.

![authorize ionos](https://github.com/M-L56/self-hosting-with-ionos/blob/d04f37d41a71a642cc8979aa8a331561be4e4a46/images/authorize_ionos.png)

We go down the page until we reach the section of DynDns, in which we clic on Post.

![DynDNS](https://github.com/M-L56/self-hosting-with-ionos/blob/d04f37d41a71a642cc8979aa8a331561be4e4a46/images/DynDNS.png)

Later we clic on try it out, and we change the default parameters with our own domain. And we will obtain this curl, so we need to create a little program with this script. 
>This command makes an HTTP POST request to the Ionos DynDNS API in order to configure or update a dynamic DNS service for the specified domains. 

![DynDNS2](https://github.com/M-L56/self-hosting-with-ionos/blob/d04f37d41a71a642cc8979aa8a331561be4e4a46/images/DynDNS2.png)

We will have to make the api key be stored in a file . env and that is in .gitignore, so that in our sript we collect from this site the api key so that no one who looks at our repository has access to our ionos.

>Inside .env
>```bash
>API_KEY="your_api_key"
>```

Create the script with bash

```bash
#!/bin/bash

# Load the file variables .env
source .env

# Make the request with curl
curl -X 'POST' \
  'https://api.hosting.ionos.com/dns/v1/dyndns' \
  -H 'accept: application/json' \
  -H "X-API-Key: $API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
  "domains": [
    "fondomarcador.com",
    "www.fondomarcador.com"
  ],
  "description": "My DynamicDns"
}'
```

In the provision of Vagrantfile we need to initialize the server, for this we introduce these two lines:
>The a2ensite command is used to enable a site configuration file on the Apache web server
```ruby
server.vm.provision "shell", inline: <<-SHELL
    sudo a2ensite fondomarcador.conf
    systemctl restart apache2
  SHELL
```

Once created our script, we must pass it to our machine and with the command crontab, which is running every five minutes, this will help us so that there are no problems with the ip.

```ruby
server.vm.provision "shell", inline: <<-SHELL
    mkdir -p /home/vagrant/scripts
    cp /vagrant/scripts/DynDNS.sh /home/vagrant/scripts
    chmod +x /home/vagrant/scripts/DynDNS.sh
    (crontab -l 2>/dev/null; echo "*/5 * * * * /home/vagrant/scripts/DynDNS.sh") | crontab -
  SHELL
```
## Virtual machine creation using Vagrant
We will create a virtual machine, which will be our server.

### 1.- Creation of the server machine
We will create a machine in debian/bookworm64:

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"
end
```

### 2.- Define the server machine
We give a static IP to our server, and configure port forwarding for http and https. At first I make insecure my machine to test that is working.

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"
  config.ssh.insert_key = false

  config.vm.define "server" do |server|
    server.vm.network "private_network", ip: "192.168.57.10"
    server.vm.network "forwarded_port", guest: 80, host: 8080
    server.vm.network "forwarded_port", guest: 443, host: 8443
  end
end
```

## Provisioning by vagrant
Has a provisioning with vagrant, where we will install and configure Apache2.

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
    SHELL
```

### Configuring Apache2
#### - apache2.conf
Copy apache2.conf from the machine.

> Inside the machine
>```bash
>cp /etc/apache2/apache2.conf /vagrant/
>```

In the provision of Vagrantfile we need to copy this file inside its path. This will be important later, but now we dont change it.

This file is inside our folder called apache2 where we will put the apache configuration files and pages

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
    SHELL
```

#### - fondomarcador.conf
We need to define a Virtual Host in Apache. 
>Virtual Hosts allow the Apache web server to host multiple websites or applications on the same machine, differentiating them by their domain name, port, or IP address. 

This is a simple configuration on port 80 of the server, later we will include an index.html, webpages and more.

```apacheconf
<VirtualHost *:80>
    ServerAdmin webmaster@fondomarcador.com
    ServerName fondomarcador.com
</VirtualHost>
```

In our Vagrantfile we need to provision with the Virtual Host configuration inside `/etc/apache2/sites-available`.

> When you use a2ensite, Apache creates a symlink in sites-enabled, pointing to the file in sites-available. This makes the site active without having to duplicate configurations or modify the file structure.

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
      cp -v /vagrant/apache2/fondomarcador.conf /etc/apache2/sites-available
    SHELL
```

#### - Webpages
We create a folder that inside we create the differents webpages
1. Index.html

At first I create a simple index.html to test the self-hosting, later I will upgrade to make looks better with the paths of the others webpages. We need to add this file inside `/var/www/html`

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
      cp -v /vagrant/apache2/fondomarcador.conf /etc/apache2/sites-available
      cp -v /vagrant/apache/webpages/index.html /var/www/html
    SHELL
```

We need to add the path of the index.html inside the virtual host

```apacheconf
<VirtualHost *:80>
    ServerAdmin webmaster@fondomarcador.com
    ServerName fondomarcador.com

    DocumentRoot /var/www/html
</VirtualHost>
```

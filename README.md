# Self hosting with IONOS
First, we need a domain from Ionos to carry out this practice. We will create a virtual machine to serve as our server and provision it with Apache2. Then, we will bind our domain to the server's IP using a bash script that will run every time the VM starts. Once created our website, we will create various web pages with different functions. 

In my case I will practice by using two types of provisioning, first with vagrant and then with ansible. This I do because in Windows ansible does not work very well due to compatibility.  
<!--(what mania I’m starting to have windows)-->

## Opening ports
Inside our router we need to open ports 80 and 443.

![ports image in router](https://github.com/M-L56/self-hosting-with-ionos/blob/12529c1b2710c5347e13eb959e802d787af783f8/images/ports.png)

## Virtual machine creation using Vagrant
We will create a virtual machine, which will be our server.

### 1. Creation of the server machine
We will create a machine in debian/bookworm64:

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"
end
```

### 2. Define the server machine
We give a static IP to our server, and configure port forwarding for http and https. At first I make insecure my machine to test that is working.

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"

  config.vm.define "server" do |server|
    server.vm.network "private_network", ip: "192.168.57.10"
    server.vm.network "forwarded_port", guest: 80, host: 8080
    server.vm.network "forwarded_port", guest: 443, host: 8443
  end
end
```

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
### Provisioning by vagrant
In the provision of Vagrantfile we need to initialize the server, for this we introduce these two lines:
>The a2ensite command is used to enable a site configuration file on the Apache web server.
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
### Provisioning by ansible

## Certification for our domain with Lets Encrypt
In my case, I’m going to certify my domain with [lets encrypt](https://letsencrypt.org/)

### Provisioning by vagrant
In our Vagrantfile provision we will install certbot with apache2 dependencies.
```ruby
server.vm.provision "shell", inline: <<-SHELL
      sudo apt install certbot python3-certbot-apache -y
    SHELL
```
The following command obtains and configures a Let’s Encrypt SSL certificate for the fondomarcador.com domain, automatically enabling HTTPS in Apache and redirecting HTTP traffic to HTTPS.
```ruby
server.vm.provision "shell", inline: <<-SHELL
      sudo apt install certbot python3-certbot-apache -y
      sudo certbot --apache --non-interactive --agree-tos --email mquepra130@ieszaidinvergeles.org -d fondomarcador.com
    SHELL
```
## Configuring Apache2
### Provisioning by vagrant
Has a provisioning with vagrant, where we will install and configure Apache2.

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
    SHELL
```

#### - apache2.conf
Copy apache2.conf from the machine.

> Inside the machine
>```bash
>cp /etc/apache2/apache2.conf /vagrant/
>```

In the provision of Vagrantfile we need to copy this file inside its path. This will be important later, but now we dont change it.

This file is inside our folder called apache2 where we will put the apache configuration files and pages.

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
We create a folder that inside we create the differents webpages.
1. Index.html

At first I create a index.html file, later we need to add this file inside `/var/www/html`.

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
      cp -v /vagrant/apache2/fondomarcador.conf /etc/apache2/sites-available
      cp -v /vagrant/apache/webpages/index.html /var/www/html
    SHELL
```

We need to add the path of the index.html inside the virtual host.

```apacheconf
<VirtualHost *:80>
    ServerAdmin webmaster@fondomarcador.com
    ServerName fondomarcador.com

    DocumentRoot /var/www/html
</VirtualHost>
```

2. 404.html

Once the 404.html file has been created, which will tell you that the page is not found, we will have to put this file in `/var/www/html`.

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
      cp -v /vagrant/apache2/fondomarcador.conf /etc/apache2/sites-available
      cp -v /vagrant/apache/webpages/index.html /var/www/html
      cp -v /vagrant/apache2/webpages/404.html /var/www/html 
    SHELL
```

We need to add the path of the 404.html inside the virtual host.

```apacheconf
<VirtualHost *:80>
    ServerAdmin webmaster@fondomarcador.com
    ServerName fondomarcador.com

    DocumentRoot /var/www/html

    ErrorDocument 404 /404.html
</VirtualHost>
```

3. logo.png

First we add a png image to our webpages folder, then add this image to the vagrant provisioning, in the path `/var/www/html`.

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
      cp -v /vagrant/apache2/fondomarcador.conf /etc/apache2/sites-available
      cp -v /vagrant/apache/webpages/index.html /var/www/html
      cp -v /vagrant/apache2/webpages/404.html /var/www/html
      cp -v /vagrant/apache2/webpages/logo.png /var/www/html 
    SHELL
```

We added to our site configuration, the following parameters for a direct installation of the file.

```apacheconf
<VirtualHost *:80>
    ServerAdmin webmaster@fondomarcador.com
    ServerName fondomarcador.com

    DocumentRoot /var/www/html

    ErrorDocument 404 /404.html

    <Files "logo.png">
        #Indicates that it is a binary file, meaning the browser will not directly display it.
        ForceType application/octet-stream
        #Sets the HTTP header so that the browser downloads the file as an attachment, rather than showing it on screen.
        Header set Content-Disposition attachment
    </Files>
</VirtualHost>
```

The Header directive requires that the mod_headers module is enabled

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
      cp -v /vagrant/apache2/fondomarcador.conf /etc/apache2/sites-available
      cp -v /vagrant/apache/webpages/index.html /var/www/html
      cp -v /vagrant/apache2/webpages/404.html /var/www/html
      sudo a2enmod headers 
      cp -v /vagrant/apache2/webpages/logo.png /var/www/html 
    SHELL
```

4. /admin

In this case, we are going to create a page where we are asked to authenticate in order to access. First, we will create the necessary pages, within the admin page there will be an image, and I thought that if someone cannot authenticate, by clicking cancel, they will be redirected to a 401 error page with our style. We will also need a .htaccess file to protect our directory with passwords. All this configuration will need to be placed in a folder to keep things organized, in my case, `/admin` inside `/var/www/html`. Next, we will look at the provisioning.

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
      cp -v /vagrant/apache2/fondomarcador.conf /etc/apache2/sites-available
      cp -v /vagrant/apache/webpages/index.html /var/www/html
      cp -v /vagrant/apache2/webpages/404.html /var/www/html
      sudo a2enmod headers 
      cp -v /vagrant/apache2/webpages/logo.png /var/www/html 
      mkdir /var/www/html/admin
      cp /vagrant/apache2/webpages/admin/.htaccess /var/www/html/admin/
      cp /vagrant/apache2/webpages/admin/admin.html /var/www/html/admin/
      cp /vagrant/apache2/webpages/admin/image.png /var/www/html/admin/
      cp /vagrant/apache2/webpages/admin/401.html /var/www/html/admin/
    SHELL
```

Next, we will need to obtain the `.htpasswd` password. To do this, we will need to access our active machine. With this command, we will ask it to store our admin password in our hidden /.htpasswd folder.

> Inside the machine
>```bash
>htpasswd -c /vagrant/.htpasswd/.htpasswd_admin admin
>```

Continuing with the practice, we will need to provision our server with this password so that the `.htaccess` file can be linked to the password.

```ruby
server.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get -y install apache2
      cp -v /vagrant/apache2/apache2.conf /etc/apache2
      cp -v /vagrant/apache2/fondomarcador.conf /etc/apache2/sites-available
      cp -v /vagrant/apache/webpages/index.html /var/www/html
      cp -v /vagrant/apache2/webpages/404.html /var/www/html
      sudo a2enmod headers 
      cp -v /vagrant/apache2/webpages/logo.png /var/www/html 
      mkdir /var/www/html/admin
      cp /vagrant/apache2/webpages/admin/.htaccess /var/www/html/admin/
      cp /vagrant/apache2/webpages/admin/admin.html /var/www/html/admin/
      cp /vagrant/apache2/webpages/admin/image.png /var/www/html/admin/
      cp /vagrant/apache2/webpages/admin/401.html /var/www/html/admin/
      # .htpasswd
      cp /vagrant/.htpasswd/.htpasswd_admin /etc/apache2/.htpasswd_admin
    SHELL
```

Now let's look at the `.htaccess` configuration:

```apacheconf
# Enable Basic Authentication
AuthType Basic
# Specify the realm (name) for the authentication prompt
AuthName "Restricted Area"
# Define the path to the .htpasswd file that stores the usernames and passwords
AuthUserFile /etc/apache2/.htpasswd_admin
# Require valid user credentials to access this directory
Require valid-user

# Custom Error Page for Unauthorized Access (401)
ErrorDocument 401 /admin/401.html
```

It will also be necessary to change the `fondomarcador.conf` file:

```apacheconf
<Directory "/var/www/html/admin">
    # Configures the authentication type as 'Basic'
    AuthType Basic
    # Name of the restricted area shown to the user
    AuthName "Restricted Area"
    # Path to the file containing user passwords
    AuthUserFile /etc/apache2/.htpasswd_admin
    # Requires the user to be authenticated to access the directory
    Require valid-user
    # Sets the default file to load in this directory
    DirectoryIndex admin.html
    # Allows overriding configurations with .htaccess in this directory
    AllowOverride All
    # Grants access to all users
    Require all granted
</Directory>
```
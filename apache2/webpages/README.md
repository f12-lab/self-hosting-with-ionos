# Webpages
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
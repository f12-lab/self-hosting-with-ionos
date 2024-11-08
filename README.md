# Self hosting with IONOS
First of all we need a domain in Ionos to perform the following practice. In this practice we will create a virtual machine that will be our server, then we will provision it with Apache2. We will then bind our domain to the ip using a python script that will start every time we start the vm.

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
      cp -v /vagrant/apache2/apache2.conf
    SHELL
```
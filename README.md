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
We give a static IP to our server, and configure port forwarding for http and https. Has a provisioning for ansible, where we will install and configure Apache2.

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"

  config.vm.define "server" do |server|
    server.vm.network "private_network", ip: "192.168.57.10"
    server.vm.network "forwarded_port", guest: 80, host: 8080
    server.vm.network "forwarded_port", guest: 443, host: 8443
    server.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook.yml"
    end
  end
end
```

## Provisioning by vagrant
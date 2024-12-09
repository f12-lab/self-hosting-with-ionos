# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Configuración básica de la VM
  config.vm.define "server" do |server|
    server.vm.box = "debian/bookworm64"
    server.vm.network "private_network", ip: "192.168.57.10"
    server.vm.network "forwarded_port", guest: 80, host: 8080
    server.vm.network "forwarded_port", guest: 443, host: 8443
    
    # Configuración de Ansible
    server.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "1.8"
      ansible.playbook = "sites.yml"
      ansible.inventory_path = "hosts"
    end
  end
end

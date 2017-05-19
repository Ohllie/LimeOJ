# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  
  config.vm.define :controller do |controller|

    controller.vm.box = "ubuntu/trusty64"
    controller.vm.hostname = "lime.controller"
    controller.vm.network :private_network, ip: "192.168.10.11"

    controller.vm.synced_folder "lime/ansible/", "/lime/ansible"

    $script = <<-SCRIPT
    
    apt-get install -y python3 software-properties-common
    apt-add-repository ppa:ansible/ansible
    apt-get update
    apt-get install -y ansible

    echo "Controller provisioned"
    SCRIPT

    controller.vm.provision "shell", inline: $script, privileged: true
    controller.vm.provision "file", source: "lime/ansible/provision_key", destination: "/home/vagrant/.ssh/id_rsa"
  end

  config.vm.define :master do |master|

    master.vm.box = "ubuntu/trusty64"
    master.vm.hostname = "lime.master"
    master.vm.network :private_network, ip: "192.168.10.12"

    $script = <<-SCRIPT

    cat /home/vagrant/.ssh/provision_key.pub >> /home/vagrant/.ssh/authorized_keys
    rm /home/vagrant/.ssh/provision_key.pub

    echo "Master provisioned"
    SCRIPT

    master.vm.provision "file", source: "lime/ansible/provision_key.pub", destination: "/home/vagrant/.ssh/provision_key.pub"
    master.vm.provision "shell", inline: $script, privileged: true
  end
end

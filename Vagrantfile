# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
 
  config.vm.define :controller do |controller|

    controller.vm.box = "ubuntu/xenial64"
    controller.vm.hostname = "controller"
    controller.vm.network :private_network, ip: "192.168.10.11"

    controller.vm.synced_folder ".", "/lime"

    $script = <<-SCRIPT
    
    apt-get install -y python3 software-properties-common
    apt-add-repository ppa:ansible/ansible
    apt-get update
    apt-get install -y ansible

    # handly link for deploy script
    ln -s /lime/lime/ansible/deploy.sh deploy.sh

    echo "Controller provisioned"
    SCRIPT

    controller.vm.provision "shell", inline: $script, privileged: true
    controller.vm.provision "file", source: "lime/ansible/provision_key", destination: "/home/ubuntu/.ssh/id_rsa"
    controller.vm.provision "shell", inline: "chmod 600 /home/ubuntu/.ssh/id_rsa", privileged: true
  end

  config.vm.define :master do |master|

    master.vm.box = "ubuntu/xenial64"
    master.vm.hostname = "master"
    master.vm.network :private_network, ip: "192.168.10.12"

    master.vm.network "forwarded_port", guest: 80, host: 8080
    master.vm.synced_folder "lime", "/lime"

    $script = <<-SCRIPT

    cat /home/ubuntu/.ssh/provision_key.pub >> /home/ubuntu/.ssh/authorized_keys
    rm /home/ubuntu/.ssh/provision_key.pub

    echo "Master provisioned"
    SCRIPT

    master.vm.provision "file", source: "lime/ansible/provision_key.pub", destination: "/home/ubuntu/.ssh/provision_key.pub"
    master.vm.provision "shell", inline: $script, privileged: true
  end
end

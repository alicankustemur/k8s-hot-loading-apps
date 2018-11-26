# -*- mode: ruby -*-
# vi: set ft=ruby :

KUBE_IP = "192.168.31.50"

Vagrant.configure(2) do |config|
  (0..0).each do |i|
    config.vm.define "kube" do |kube|
      kube.vm.box = "geerlingguy/ubuntu1604"
      kube.vm.hostname = "kube"
      kube.vm.network "private_network", ip: "#{KUBE_IP}"
      kube.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "main.yaml"
        ansible.galaxy_role_file = 'requirements.yaml'
        ansible.inventory_path = "/vagrant/inventory"
        ansible.become = true
        ansible.raw_arguments = ["-v"]
      end

      kube.vm.provider "virtualbox" do |vb|
        vb.memory = 2048
        vb.cpus = 2
      end
      
    end  
  end  
end

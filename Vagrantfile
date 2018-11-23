# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  (0..0).each do |i|
    config.vm.box = "geerlingguy/ubuntu1604"
    config.vm.define "kube" do |kube|
      kube.vm.hostname = "kube"
      kube.vm.network "private_network", ip: "192.168.33.71"
      kube.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "main.yml"
        ansible.galaxy_role_file = 'requirements.yml'
        ansible.limit = "all"
        ansible.become = true
        ansible.raw_arguments = ["-v"]
        ansible.groups = {
          "kubernetes" => ["kube"],
          "kubernetes_master" => ["kube"],
          "kubernetes_master:vars" => {
            kubernetes_role: "master",
            kubernetes_apiserver_advertise_address: "192.168.33.71"
          }
        }
      end  

      kube.vm.provider "virtualbox" do |vb|
        vb.memory = 1024
        vb.cpus = 1
      end
      
    end  
  end  
end

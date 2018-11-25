
## k8s Hot Loading Apps ( Beta )

### Background
We want only focus to the code when developing applications in any language.
But for that we always want the environment to work.
This repo only allows you to focus on your code.(like [Webpack Hot Module Replacement](https://webpack.js.org/concepts/hot-module-replacement/))

Our application will running as container.

We only will change the code then our application's configuration on `Kubernetes` will notice the changes in the code, and it will recreate new container with include new code.

Supported Languages:
- Python 

## Getting Started

This `README` file is inside a folder that contains a `Vagrantfile` (hereafter this folder shall be called the [vagrant_root]), which tells Vagrant how to set up your virtual machine in VirtualBox.

To use the vagrant file, you will need to have done the following:

  1. Download and Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
  2. Download and Install [Vagrant](https://www.vagrantup.com/downloads.html)

### Infrastructure
`Vagrant` is infrastructure orchestrator for development environments.
`Ansible` is very simplfy infrastructure provisioning tools.
`Vagrant` and `VirtualBox` (or some other VM provider) can be used to quickly build or rebuild virtual servers.
`Kubernetes` is top level container orchestrator.
`Docker` is most popular container platform.



You just need to install `Vagrant` and `VirtualBox`.

You can cd into any of the included directories and run `vagrant up`, and a generic `Linux VM` will be booted and configured in a few minutes. 

This Vagrant profile installs [Kubernetes](https://kubernetes.io) and [Docker](https://docker.io) using the [Ansible](http://www.ansible.com/) provisioner.

Used Versions:

- Kubernetes : `1.10`
- Docker : `17.03.0~ce-0`
 ( Because Kubernetes `1.10` version  validated docker versions `1.11.2` to `1.13.1` and `17.03.x`)
 [Kubernetes 1.10 CHANGELOG - External Dependencies](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.10.md#external-dependencies)


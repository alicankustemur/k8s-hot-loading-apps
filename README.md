
# k8s Hot Loading Apps ( Beta )

![k8s-hot-loadings GIF](k8s-hot-loading-apps.gif)

## Background
We want only focus to the code when developing applications in any language.
But for that we always want the environment to work.
This repo only allows you to focus on your code.(like [Webpack Hot Module Replacement](https://webpack.js.org/concepts/hot-module-replacement/))

Our application will running as container.

We only will change the code then our application's configuration on `Kubernetes` will notice the changes in the code, and it will recreate new container with include new code.

Supported Languages Now:
- Python 

## Getting Started

This `README` file is inside a folder that contains a `Vagrantfile` (hereafter this folder shall be called the [vagrant_root]), which tells Vagrant how to set up your virtual machine in VirtualBox.

To use the vagrant file, you will need to have done the following:

  1. Download and Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
  2. Download and Install [Vagrant](https://www.vagrantup.com/downloads.html)


Setting up your hosts file
You need to modify your host machine's hosts file

Mac/Linux: `/etc/hosts`

Windows: `%systemroot%\system32\drivers\etc\hosts` 

adding the line below:

```
192.168.31.50  kube
```

You just need to install `Vagrant` and `VirtualBox`.

You can cd into any of the included directories and run `vagrant up`, and a generic `Linux VM` will be booted and configured in a few minutes. 

Once `Vagrant` provisioning finished, run `vagrant ssh` and log into `kube` VM then check pods statuses. 

```
vagrant@kube:~$ kubectl get pods --all-namespaces
NAMESPACE     NAME                            READY     STATUS    RESTARTS   AGE
default       mysql-675576cbd8-8nwlj          1/1       Running   2          1h
default       python-mysql-566df64fcb-jwx66   1/1       Running   4          40m
kube-system   etcd-kube                       1/1       Running   2          1h
kube-system   kube-apiserver-kube             1/1       Running   2          1h
kube-system   kube-controller-manager-kube    1/1       Running   2          1h
kube-system   kube-dns-86f4d74b45-r9kc9       3/3       Running   6          1h
kube-system   kube-flannel-ds-amd64-xpkx7     1/1       Running   2          1h
kube-system   kube-proxy-4dlvr                1/1       Running   2          1h
kube-system   kube-scheduler-kube             1/1       Running   2          1h
kube-system   weave-net-km79d
```

To see `python-mysql Application`, type `kube:31000` in the browser .


## Infrastructure
`Vagrant` is infrastructure orchestrator for development environments.
`Ansible` is very simplfy infrastructure provisioning tools.
`Vagrant` and `VirtualBox` (or some other VM provider) can be used to quickly build or rebuild virtual servers.
`Kubernetes` is top level container orchestrator.
`Docker` is most popular container platform.

This Vagrant profile installs [Kubernetes](https://kubernetes.io) and [Docker](https://docker.io) using the [Ansible](http://www.ansible.com/) provisioner.

It has one playbook file `main.yml` and all provisioning from here.
We using [geerlingguy](https://github.com/geerlingguy) [Kubernetes](https://github.com/geerlingguy/ansible-role-kubernetes) and [Docker](https://github.com/geerlingguy/ansible-role-docker) Ansible Roles.

## Kubernetes

Cluster has only one `master` and it hasn't `worker` nodes.
All pods running on `master` node. This option comes from `Kubernetes Ansible Role` variable `kubernetes_allow_pods_on_master`.

Swap disabled on `kube` VM.
 Official reason:  [Kubernetes - Before you begin](https://kubernetes.io/docs/setup/independent/#before-you-begin)
 ```
 Swap disabled. You MUST disable swap in order for the kubelet to work properly.
```
 
### - Network
  We apply [Weave Net Kubernetes CNI Network Plugin](https://www.weave.works/docs/net/latest/kubernetes/kube-addon/) to  `Kubernetes Cluster`.

[Choosing a CNI Network Provider for Kubernetes](https://chrislovecnm.com/kubernetes/cni/choosing-a-cni-provider/)

Because `Kubernetes` default networking provider, `kubenet`, is a simple network plugin.
  

Kubernetes definitions are in `k8s-definitions` folder.

```
vagrant@kube:/vagrant/k8s-definitions$ tree
.
├── mysql
│   ├── deployment.yaml
│   ├── persistent-volume-claim.yaml
│   ├── persistent-volume.yaml
│   └── service.yaml
├── python-mysql
│   ├── deployment.yaml
│   ├── persistence-volume.yaml
│   ├── persistent-volume-claim.yaml
│   └── service.yaml
└── weaveworks.yaml

2 directories, 9 files
```

### - Definitions

#### mysql

```
vagrant@kube:/vagrant/k8s-definitions/mysql$ tree
.
├── deployment.yaml
├── persistent-volume-claim.yaml
├── persistent-volume.yaml
└── service.yaml

0 directories, 4 files
```
All definition labels are `app:python-mysql` and only mysql `Deployment` definition has `name:mysql` label. :

```
labels:
    app: python-mysql
    name: mysql
```

more : [Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)

`deployment.yaml`
```
spec:
  terminationGracePeriodSeconds: 2
```
If the pod give an error, it graceful shutdowns and restarts.

`service.yaml`

```
apiVersion: v1
kind: Service
metadata:
  name: mysql
```
`Kubernetes service name` also determines own `DNS`.

Pods access `mysql` service with this way in same namespace.

`mysql.default.svc` is `mysql` service `DNS`.

[Dns for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pods)

[Kubernetes DNS-Based Service Discovery](https://github.com/kubernetes/dns/blob/master/docs/specification.md)

`PersistentVolume` mounts `/home/vagrant/mysql-data/` to `/var/lib/mysql`. 

 The mysql container will use the `PersistentVolumeClaim` and mount the persistent disk at `/var/lib/mysql` inside the container.

### - Test mysql persistent data

With `PersistentVolumes`, your data lives outside the application container. Run the following command in `kube VM`

Now, delete the `mysql` Pod by running:

```
kubectl delete pod  -l name=mysql
```

then check persist data in new Pod.

```
 kubectl exec -it $(kubectl get pod -l name=mysql -o name | sed 's/pod\///g') -- bash

root@mysql-6887764894-bbkvh:/# mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 1
Server version: 5.6.42 MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> use root; select * from scores;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
+-------+
| score |
+-------+
|  1234 |
|  1234 |
+-------+
2 rows in set (0.00 sec)
```
The data is persisted even though you deleted your Pod and the Pod is scheduled to another instance in your cluster.


### python-mysql

```
vagrant@kube:/vagrant/k8s-definitions/python-mysql$ tree
.
├── deployment.yaml
├── persistence-volume.yaml
├── persistent-volume-claim.yaml
└── service.yaml

0 directories, 4 files
```

`persistence-volume.yaml` 

```
---
kind: PersistentVolume
apiVersion: v1
metadata:
  name: code
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/vagrant/python-mysql/"
---
```

Our application code is in `/vagrant/python-mysql/`.

`PersistentVolume` mounts `/vagrant/python-mysql/` to `/code`. 

```
  volumeMounts:
  - mountPath: /code
    name: code
volumes:
- name: code
  persistentVolumeClaim:
    claimName: code
```


`deployment.yaml`

mysql connection environments

```
env:
  - name: MYSQL_USERNAME
    value: root 
  - name: MYSQL_PASSWORD
    value: vb7jKUVapNLyykBv 
  - name: MYSQL_INSTANCE_NAME
    value: root 
  - name: MYSQL_TCP_ADDR
    value: mysql.default.svc 
  - name: MYSQL_TCP_PORT
    value: "3306"
```
`mysql.default.svc` is mysql service DNS.

```
spec:
  terminationGracePeriodSeconds: 2
```
If the pod give an error, it graceful shutdowns and restarts.

```
image: flask:latest
imagePullPolicy: Never
```
`flask:latest` image builded with `python-mysql/Dockerfile`.


`Dockerfile`
```
FROM alpine:3.7

ADD . /code

WORKDIR /code

# All packages are versioned for idempotent.
RUN apk add --update python2==2.7.15-r2 py-pip==9.0.1-r1 py-mysqldb==1.2.5-r0

# All packages are versioned for idempotent.
RUN pip install Flask==1.0.2 MySQL-python==1.2.5 gunicorn==19.9.0
``` 

`Flask` is a micro web framework written in `Python`.

`Gunicorn` 'Green Unicorn' is a `Python WSGI HTTP Server` for UNIX. ( Default `Flask` Serving isn't recommended for production grade. )




```
args:
- /bin/sh
- -c
- cp application.py temp.py; gunicorn --bind 0.0.0.0:3000 application:application
```

In here Pod firstly copys `application.py` ( in `python-mysql` folder) to `temp.py` and runs gunicorn application server with `application.py`.

If the `application.py` code is changes when Pod lifecycle it `livenessProbe` runs the following command.

```
livenessProbe:
  exec:
    command:
    - /bin/sh
    - -c
    - '`/usr/bin/cmp -s /code/application.py /code/temp.py`'    
```

`/usr/bin/cmp` binary is compares the contents of two files and reports the first character that differs. If the files ( `application.py` and `temp.py` ) are different, it exists with a code other than `0`.

`livenessProbe` notices it and restarts Pod.
In this way the new `application.py` code runs with Pod commands and this is repeated continuously.

For Example:

![k8s-hot-loadings GIF](k8s-hot-loading-apps.gif)

Used Versions:

- Kubernetes : `1.10`
- Docker : `17.03.0~ce-0`
 ( Because Kubernetes `1.10` version  validated docker versions `1.11.2` to `1.13.1` and `17.03.x`)
 [Kubernetes 1.10 CHANGELOG - External Dependencies](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.10.md#external-dependencies)


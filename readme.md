# get-of-metrics.py

Get of Metrics version K8s

## Overview

get-of-metrics is a Python script for dealing the Broadcom switch metrics to extract from commandline, parse the metrics and expose them to be processed by Prometheus and Grafana.

This version of the scipt works as a Prometheus Exporter.

Use the secret.yml file to intruduce a remote machine and the delay time.

## Installation for only the script

Python 3.7 and above need to be installed.

paramiko, re, threading, json, prometheus_client and time libraries are used in this script. json, re, threading and time are the standart libraries. prometheus_client, paramiko need to be installed.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 

```bash
pip install paramiko
pip install prometheus_client
```

If you install with .deb package (which is already provided) it will install all Python packages by itself.

Performs installation.

```bash 
apt install ./get-of-metrics.deb
```

If you install script solely you can use these commends to activate get-of-metrics service. get-of-metrics service file is already provided in the .deb package so while installation it will install the service file so you dont need to be bother yourself to create a service file for the script.

Starts the script service

```bash
systemctl start get-of-metrics
```

Enables the service runs itself automatically after every reboot.

```bash
systemctl enables get-of-metrics
```
## Guide for Grafana, Prometheus and get-of-metrics

`https://medium.com/@eminaktas/kubectl-minikube-prometheus-grafana-and-get-of-metrics-kurulum-ve-%C3%A7al%C4%B1%C5%9Ft%C4%B1r%C4%B1lmas%C4%B1-56c7a1a6293e`

## Installation with Kubernetes for only the script

All the files for Kubernetes are provided. Before executing the code, edit `secret.yml` to introduce the remote machine.

```bash
kubectl apply -k .
```

## Installation with Dockerfile for only the script

Dockerfile is provided in the file named `Dockerfile`. By using the docker file you can make create the docker image.

Builds the docker image locally. It also uploaded in Docker Hub.

```bash
docker build -t get-of-metrics .
```
Runs the image as a container and pull the image with requeired files from Dockerhub.
`-d` runs as a deamon.
`--name` names the script.
`-v` in order to have access the files.
`-p` expose the port to the port number on the left.
At the last of the command we give the image name which is `eminaktas/get-of-metrics`

```bash
docker run -d --name get-of-metrics -p 8080:8080 -v ./logs:/get-of-metrics/logs -e ALIAS=enter-alias -e HOST=enter-host -e USER=enter-user -e PASSWORD=enter-password -e DELAY=enter-delay(default-1-sec) eminaktas/get-of-metrics:k8s
```

Getting acces to container

```bash
docker exec -it get-of-metrics bash
```

## Extra commands

Tracking the life cycle of get-of-metrics service

```bash
systemctl status get-of-metrics
```

Performs uninstallation.

```bash
apt remove get-of-metrics
```

## Required commands and information for creation and installation dpkg/apt

Creating and copying required files and folders for installation

```bash
mkdir ./get-of-metrics
mkdir ./get-of-metrics/DEBIAN
mkdir ./get-of-metrics/etc
mkdir ./get-of-metrics/etc/systemd
mkdir ./get-of-metrics/etc/systemd/system
mkdir ./get-of-metrics/home/get-of-metrics
mkdir ./get-of-metrics/home/get-of-metrics/bin
mkdir ./get-of-metrics/var
mkdir ./get-of-metrics/var/log
mkdir ./get-of-metrics/var/log/get-of-metrics
cp ./get-of-metrics.py ./get-of-metrics/usr/bin/get-of-metrics
```

The contents of the files are available in the ./get-of-metrics/DEBIAN folder and ./get-of-metrics/etc/systemd/systemd/get-of-metrics.service.

```bash
vi ./get-of-metrics/etc/systemd/systemd/get-of-metrics.service
vi ./get-of-metrics/DEBIAN/prerm
vi ./get-of-metrics/DEBIAN/control
```

Regulates the privileges of created prerm and control. If it is not edited, it may fail while creating .deb.

```bash
chmod 775 ./get-of-metrics/DEBIAN/prerm
chmod 775 ./get-of-metrics/DEBIAN/control
```

Creates a deb file for installation.

```bash
dpkg-deb --build get-of-metrics
```
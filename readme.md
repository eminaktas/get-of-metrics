# get-of-metrics.py

Get of Metrics version 3

## Overview

get-of-metrics is a Python script for dealing the Broadcom switch metrics to extract from commandline, parse the metrics and expose them to be processed by Prometheus and Grafana.

This version works as a Prometheus Exporter.

Required parameters to introduce machines in the setup. Use `connection-parameters.json` file to intruduce the remote machines and the delay time.

## Installation for only the script

Python 3.7 and above need to be installed.

argparse, paramiko, systemd, re, threading, json, prometheus_client, datetime and time libraries are used in this script. argparse, json, re, threading, datetime and time are the standart libraries. prometheus_client, paramiko and systemd need to be installed.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 

```bash
pip install paramiko
pip install systemd
pip install prometheus_client
```

Performs installation.

```bash 
apt install ./get-of-metrics.deb
```

Performs uninstallation.

```bash
apt remove get-of-metrics
```

## Installation with Dockerfile for only the script

Dockerfile is provided in the file named `Dockerfile`. By using the docker file you can make create the docker image.

Builds the docker image. 

```bash
docker build -t get-of-metrics .
```
Runs the image.
`-d` runs as a deamon.
`--name` names the script.
`--privileged` gives access to all deviced. Needed to activate the service in conatiner otherwise it does not work.
`-v` in order to save, access and modify the datas.
`-p` expose the port to the port number on the left.
At the last of the command we give the image name which is `get-of-metrics`

```bash
docker run -d --name get-of-metrics --privileged -p 8000:8000 -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v ./file:/home/get-of-metrics -v ./logs:/var/log/get-of-metrics -v get-of-metrics
```

Getting acces to container

```bash
docker exec -it get-of-metrics bash
```

## Installation with Docker Compose for Prometheus, Grafana and the script

Docker Compose file is provided in the file named docker-compose.yml.

Builds the docker containers as a package.

```bash
docker-compose -f docker-compose.yml up
```

Getting acces to container

```bash
docker exec -it custom-metrics sh
docker exec -it grafana sh
docker exec -it prometheus sh
```

## Extra commands

Tracking the life cycle of get-of-metrics service

```bash
systemctl status get-of-metrics
```

Clears recorded logs. 

```bash
journalctl --vacuum-time=2d
```

Access to logs. -u access to our daemon log entries. -b shows us the entries from the last boot.

```bash
journalctl -b -u get-of-metrics
```

## Required commands and information for creation and installation dpkg/apt

Creating and copying required files and folders for installation

```bash
mkdir ./get-of-metrics
mkdir ./get-of-metrics/DEBIAN
mkdir ./get-of-metrics/usr
mkdir ./get-of-metrics/usr/bin
mkdir ./get-of-metrics/usr/bin/get-of-metrics
mkdir ./get-of-metrics/etc
mkdir ./get-of-metrics/etc/systemd
mkdir ./get-of-metrics/etc/systemd/system
mkdir ./get-of-metrics/home/get-of-metrics
mkdir ./get-of-metrics/var
mkdir ./get-of-metrics/var/log
mkdir ./get-of-metrics/var/log/get-of-metrics
cp ./get-of-metrics.py ./get-of-metrics/usr/bin/get-of-metrics
cp ./family_of_metrics.py ./get-of-metrics/usr/bin/get-of-metrics
cp ./collector_of_metrics.py ./get-of-metrics/usr/bin/get-of-metrics
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